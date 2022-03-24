from unittest import TestCase
from unittest.mock import create_autospec

from awsiot.iotshadow import IotShadowClient, ShadowState


class ShadowStateToAndFromTest(TestCase):

    def test_update_reboot_requested_state(self):
        expected_state = ShadowState.from_payload({"reported": {"deviceAgent": {"rebootRequired": True}}})
        assert {"reported": {"deviceAgent": {"rebootRequired": True}}} == expected_state.to_payload()
