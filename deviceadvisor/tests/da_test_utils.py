# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
import os
from enum import Enum
from uuid import uuid4

class TestType(Enum):
    CONNECT = 1
    SUB_PUB = 2
    SHADOW = 3

class DATestUtils:
    endpoint = os.getenv('DA_ENDPOINT')
    certificatePath = os.getenv('DA_CERTI')
    keyPath = os.getenv('DA_KEY')
    topic = os.getenv('DA_TOPIC')
    thing_name = os.getenv('DA_THING_NAME')
    shadowProperty = os.getenv('DA_SHADOW_PROPERTY')
    shadowValue = os.getenv('DA_SHADOW_VALUE_SET')

    @classmethod
    def valid(cls, test_type):
        if (not (cls.endpoint and cls.certificatePath and cls.keyPath)):
            return False

        if (not cls.topic and test_type == TestType.SUB_PUB):
            return False

        if (not (cls.thing_name and cls.shadowProperty and cls.shadowValue) and test_type == TestType.SHADOW):
            return False

        return True

    @classmethod
    def generate_client_id(_self, postfix):
        return "test-DA" + str(uuid4()) + postfix
