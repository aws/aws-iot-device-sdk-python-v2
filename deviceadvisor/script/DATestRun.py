import boto3
import uuid
import json
import os
import subprocess
import re
import random
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

# Export the testing log and upload it to S3 bucket
def process_logs(log_group, log_stream, thing_name):
    logs_client = boto3.client('logs')
    response = logs_client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream
    )
    log_file = "DA_Log_Python_" + thing_name + ".log"
    f = open(log_file, 'w')
    for event in response["events"]:
        f.write(event['message'])
    f.close()

    try:
        secrets_client = boto3.client(
            "secretsmanager", region_name=os.environ["AWS_DEFAULT_REGION"])
        s3_bucket_name = secrets_client.get_secret_value(SecretId="ci/DeviceAdvisor/s3bucket")["SecretString"]
        s3.Bucket(s3_bucket_name).upload_file(log_file, log_file)
        print("[Device Advisor] Device Advisor Log file uploaded to "+ log_file)
    except Exception:
        print ("[Device Advisor] Error: could not store log in S3 bucket!")

    os.remove(log_file)
    print("[Device Advisor] Device Advisor Log file uploaded to "+ log_file)

# Sleep for a random time between base and bax
def sleep_with_backoff(base, max):
    sleep(random.randint(base,max))

##############################################
# Initialize variables
# create aws clients
try:
    client = boto3.client('iot', region_name="us-east-1")
    dataClient = boto3.client('iot-data', region_name="us-east-1")
    deviceAdvisor = boto3.client('iotdeviceadvisor', region_name="us-east-1")
    s3 = boto3.resource('s3')
except Exception as ex:
    print ("[Device Advisor] Error: could not create boto3 clients.")
    print (ex)
    exit(-1)

# const
BACKOFF_BASE = 5
BACKOFF_MAX = 10
# 60 minutes divided by the maximum back-off = longest time a DA run can last with this script.
MAXIMUM_CYCLE_COUNT = (3600 / BACKOFF_MAX)

# Did Device Advisor fail a test? If so, this should be true
did_at_least_one_test_fail = False

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
# Run device advisor
for test_name in DATestConfig['tests']:
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
        print("[Device Advisor] Info: Started to create thing...")
        create_thing_response = client.create_thing(
            thingName=thing_name
        )
        os.environ["DA_THING_NAME"] = thing_name

    except Exception as e:
        print("[Device Advisor] Error: Failed to create thing: " + thing_name)
        exit(-1)


    ##############################################
    # create certificate and keys used for testing
    try:
        print("[Device Advisor] Info: Started to create certificate...")
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

    except Exception:
        try:
            client.delete_thing(thingName = thing_name)
        except Exception:
            print("[Device Advisor] Error: Could not delete thing.")
        print("[Device Advisor] Error: Failed to create certificate.")
        exit(-1)

    certificate_arn = create_cert_response['certificateArn']
    certificate_id = create_cert_response['certificateId']

    ##############################################
    # attach policy to certificate
    try:
        secrets_client = boto3.client(
            "secretsmanager", region_name=os.environ["AWS_DEFAULT_REGION"])
        policy_name = secrets_client.get_secret_value(SecretId="ci/DeviceAdvisor/policy_name")["SecretString"]
        client.attach_policy (
            policyName= policy_name,
            target = certificate_arn
        )
    except Exception as ex:
        print (ex)
        delete_thing_with_certi(thing_name, certificate_id, certificate_arn )
        print("[Device Advisor] Error: Failed to attach policy.")
        exit(-1)

    ##############################################
    # attach certification to thing
    try:
        print("[Device Advisor] Info: Attach certificate to test thing...")
        # attache the certificate to thing
        client.attach_thing_principal(
            thingName = thing_name,
            principal = certificate_arn
        )

    except Exception:
        delete_thing_with_certi(thing_name, certificate_id ,certificate_arn )
        print("[Device Advisor] Error: Failed to attach certificate.")
        exit(-1)

    try:
        ######################################
        # set default shadow, for shadow update, if the
        # shadow does not exists, update will fail
        print("[Device Advisor] Info: About to update shadow.")
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
        print("[Device Advisor] Info: About to wait for shadow update.")
        while(get_shadow_response is None):
            get_shadow_response = dataClient.get_thing_shadow(thingName = thing_name)

        # start device advisor test
        # test_start_response
        # {
        # 'suiteRunId': 'string',
        # 'suiteRunArn': 'string',
        # 'createdAt': datetime(2015, 1, 1)
        # }
        print("[Device Advisor] Info: Start device advisor test: " + test_name)
        sleep_with_backoff(BACKOFF_BASE, BACKOFF_MAX)
        test_start_response = deviceAdvisor.start_suite_run(
            suiteDefinitionId=DATestConfig['test_suite_ids'][test_name],
            suiteRunConfiguration={
                'primaryDevice': {
                    'thingArn': create_thing_response['thingArn'],
                },
                'parallelRun': True
        })

        # get DA endpoint
        print("[Device Advisor] Info: Getting Device Advisor endpoint.")
        endpoint_response = deviceAdvisor.get_endpoint(
            thingArn = create_thing_response['thingArn']
        )
        os.environ['DA_ENDPOINT'] = endpoint_response['endpoint']

        cycle_number = 0
        while True:
            cycle_number += 1
            if (cycle_number >= MAXIMUM_CYCLE_COUNT):
                print(f"[Device Advisor] Error: {cycle_number} of cycles lasting {BACKOFF_BASE} to {BACKOFF_MAX} seconds have passed.")
                raise Exception(f"ERROR - {cycle_number} of cycles lasting {BACKOFF_BASE} to {BACKOFF_MAX} seconds have passed.")

            # Add backoff to avoid TooManyRequestsException
            sleep_with_backoff(BACKOFF_BASE, BACKOFF_MAX)
            print ("[Device Advisor] Info: About to get Device Advisor suite run.")
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
                print ("[Device Advisor] Info: About to get start Device Advisor companion test application.")
                exe_path = os.path.join("deviceadvisor/tests/",DATestConfig['test_exe_path'][test_name])
                result = subprocess.run('python3 ' + exe_path, timeout = 60*2, shell = True)
            # If the test finalizing then store the test result
            elif (test_result_responds['status'] != 'RUNNING'):
                test_result[test_name] = test_result_responds['status']
                # If the test failed, upload the logs to S3 before clean up
                if(test_result[test_name] != "PASS"):
                    print ("[Device Advisor] Info: About to upload log to S3.")
                    log_url = test_result_responds['testResult']['groups'][0]['tests'][0]['logUrl']
                    group_string = re.search('group=(.*);', log_url)
                    log_group = group_string.group(1)
                    stream_string = re.search('stream=(.*)', log_url)
                    log_stream = stream_string.group(1)
                    process_logs(log_group, log_stream, thing_name)
                delete_thing_with_certi(thing_name, certificate_id ,certificate_arn)
                break
    except Exception:
        delete_thing_with_certi(thing_name, certificate_id ,certificate_arn)
        print("[Device Advisor] Error: Failed to test: "+ test_name)
        did_at_least_one_test_fail = True
        exit(-1)

##############################################
# print result and cleanup things
print(test_result)
failed = False
for test in test_result:
    if(test_result[test] != "PASS" and
    test_result[test] != "PASS_WITH_WARNINGS"):
        print("[Device Advisor] Error: Test \"" + test + "\" Failed with status:" + test_result[test])
        failed = True
if failed:
    # if the test failed, we dont clean the Thing so that we can track the error
    exit(-1)

if (did_at_least_one_test_fail == True):
    print("[Device Advisor] Error: At least one test failed!")
    exit(-1)

exit(0)
