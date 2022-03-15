import boto3
import uuid
import json
import os
import subprocess
import platform
from time import sleep

##############################################
# Cleanup Certificates and Things and created certificate and private key file
def delete_thing_with_certi(thingName, certiId, certiArn):
    client.detach_thing_principal(
        thingName = thingName,
        principal = certiArn)
    client.update_certificate(
    certificateId =certiId,
    newStatus ='INACTIVE')
    client.delete_certificate(certificateId = certiId, forceDelete = True)
    client.delete_thing(thingName = thingName)
    os.remove(os.environ["DA_CERTI"])
    os.remove(os.environ["DA_KEY"])


##############################################
# Initialize variables
# create aws clients
client = boto3.client('iot')
dataClient = boto3.client('iot-data')
deviceAdvisor = boto3.client('iotdeviceadvisor')

# load test config
f = open('deviceadvisor/script/DATestConfig.json')
DATestConfig = json.load(f)
f.close()

# create an temporary certificate/key file path
certificate_path = os.path.join(os.getcwd(), 'certificate.pem.crt')
key_path = os.path.join(os.getcwd(), 'private.pem.key')

# load environment variables requried for testing
shadowProperty = os.environ['DA_SHADOW_PROPERTY']
shadowDefault = os.environ['DA_SHADOW_VALUE_DEFAULT']

# test result
test_result = {}

##############################################
# create a test thing 
thing_name = "DATest_" + str(uuid.uuid4())
try:
    # create_thing_response:
    # {
    # 'thingName': 'string',
    # 'thingArn': 'string',
    # 'thingId': 'string'
    # }
    print("[Device Advisor]Info: Started to create thing...")
    create_thing_response = client.create_thing(
        thingName=thing_name
    )
    os.environ["DA_THING_NAME"] = thing_name
    
except Exception as e:
    print("[Device Advisor]Error: Failed to create thing: " + thing_name)
    exit(-1)


##############################################
# create certificate and keys used for testing
try:
    print("[Device Advisor]Info: Started to create certificate...")
    # create_cert_response:
    # {
    # 'certificateArn': 'string',
    # 'certificateId': 'string',
    # 'certificatePem': 'string',
    # 'keyPair': 
    #   {
    #     'PublicKey': 'string',
    #     'PrivateKey': 'string'
    #   }
    # }
    create_cert_response = client.create_keys_and_certificate(
        setAsActive=True
    )
    # write certificate to file
    f = open(certificate_path, "w")
    f.write(create_cert_response['certificatePem'])
    f.close()

    # write private key to file
    f = open(key_path, "w")
    f.write(create_cert_response['keyPair']['PrivateKey'])
    f.close()
    
    # setup environment variable 
    os.environ["DA_CERTI"] = certificate_path
    os.environ["DA_KEY"] = key_path

except:
    client.delete_thing(thingName = thing_name)
    print("[Device Advisor]Error: Failed to create certificate.")
    exit(-1)

##############################################
# attach certification to thing
try:
    print("[Device Advisor]Info: Attach certificate to test thing...")
    # attache the certificate to thing
    client.attach_thing_principal(
        thingName = thing_name,
        principal = create_cert_response['certificateArn']
    )

    certificate_arn = create_cert_response['certificateArn']
    certificate_id = create_cert_response['certificateId']

except:
    delete_thing_with_certi(thing_name, certificate_id ,certificate_arn )
    print("[Device Advisor]Error: Failed to attach certificate.")
    exit(-1)


##############################################
# Run device advisor
for test_name in DATestConfig['tests']:
    try:
        ######################################
        # set default shadow, for shadow update, if the
        # shadow does not exists, update will fail
        payload_shadow = json.dumps(
        {
        "state": {
            "desired": {
                shadowProperty: shadowDefault
                },
            "reported": {
                shadowProperty: shadowDefault
                }
            }
        })
        shadow_response = dataClient.update_thing_shadow(
            thingName = thing_name,
            payload = payload_shadow)
        get_shadow_response = dataClient.get_thing_shadow(thingName = thing_name)
        # make sure shadow is created before we go to next step
        while(get_shadow_response is None): 
            get_shadow_response = dataClient.get_thing_shadow(thingName = thing_name)
        
        # start device advisor test
        # test_start_response
        # {
        # 'suiteRunId': 'string',
        # 'suiteRunArn': 'string',
        # 'createdAt': datetime(2015, 1, 1)
        # }
        print("[Device Advisor]Info: Start device advisor test: " + test_name)
        test_start_response = deviceAdvisor.start_suite_run(
        suiteDefinitionId=DATestConfig['test_suite_ids'][test_name],
        suiteRunConfiguration={
            'primaryDevice': {
                'thingArn': create_thing_response['thingArn'],
            },
            'parallelRun': True
        })

        # get DA endpoint
        endpoint_response = deviceAdvisor.get_endpoint(
            thingArn = create_thing_response['thingArn']
        )
        os.environ['DA_ENDPOINT'] = endpoint_response['endpoint']

        while True:
            # sleep for 1s every loop to avoid TooManyRequestsException
            sleep(1)
            test_result_responds = deviceAdvisor.get_suite_run(
                suiteDefinitionId=DATestConfig['test_suite_ids'][test_name],
                suiteRunId=test_start_response['suiteRunId']
            )
            # If the status is PENDING or the responds does not loaded, the test suite is still loading
            if (test_result_responds['status'] == 'PENDING' or
            len(test_result_responds['testResult']['groups']) == 0 or # test group has not been loaded
            len(test_result_responds['testResult']['groups'][0]['tests']) == 0 or #test case has not been loaded
            test_result_responds['testResult']['groups'][0]['tests'][0]['status'] == 'PENDING'):
                continue
            
            # Start to run the test sample after the status turns into RUNNING
            elif (test_result_responds['status'] == 'RUNNING' and 
            test_result_responds['testResult']['groups'][0]['tests'][0]['status'] == 'RUNNING'):
                working_dir = os.getcwd()
                os.chdir(exe_path)
                result = subprocess.run(['python3', DATestConfig['test_exe_path'][test_name]], timeout = 60*5, shell = True)
                # mvn compile exec:java -pl deviceadvisor/tests/MQTTConnect -Dexec.mainClass=MQTTConnect.MQTTConnect
                # mvn exec:java -Dexec.mainClass="com.example.Main" 
                os.chdir(working_dir)
            # If the test finalizing or store the test result
            elif (test_result_responds['status'] != 'RUNNING'):
                test_result[test_name] = test_result_responds['status']
                break
    except Exception as e:
        print("[Device Advisor]Error: Failed to test: "+ test_name + e)
        exit(-1)

##############################################
# print result and cleanup things
print(test_result)
failed = False
for test in test_result:
    if(test_result[test] != "PASS" and
    test_result[test] != "PASS_WITH_WARNINGS"):
        print("[Device Advisor]Error: Test \"" + test + "\" Failed with status:" + test_result[test])
        failed = True
if failed:
    # if the test failed, we dont clean the Thing so that we can track the error
    exit(-1)

delete_thing_with_certi(thing_name, certificate_id ,certificate_arn )
exit(0)
