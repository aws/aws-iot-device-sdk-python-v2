from unittest import TestCase

from awsiot.iotshadow import IotShadowClient, ShadowState


class ShadowStateToAndFromTest(TestCase):

    def test_to_and_from_payload_parity(self):
        expected_state = ShadowState.from_payload({"reported": {"deviceAgent": {"rebootRequired": True}}})
        assert {"reported": {"deviceAgent": {"rebootRequired": True}}} == expected_state.to_payload()
