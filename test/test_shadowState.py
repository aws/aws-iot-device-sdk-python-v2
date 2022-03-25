from unittest import TestCase

from awsiot.iotshadow import ShadowState


class ShadowTest(TestCase):

    def test_shadow_state_payload_filled(self):
        testState = ShadowState.from_payload({
            "reported": {"Color": "Red"},
            "desired": {"Color": "Blue"}
        })
        compareState = ShadowState(
            reported={"Color": "Red"},
            desired={"Color": "Blue"}
        )
        self.assertTrue(testState.to_payload() == compareState.to_payload())

    def test_shadow_state_payload_partial_filled(self):
        testState = ShadowState.from_payload({
            "reported": {"Color": "Red"}
        })
        compareState = ShadowState(
            reported={"Color": "Red"}
        )
        self.assertEqual(testState.to_payload(), compareState.to_payload())

    def test_shadow_state_payload_can_send_null(self):
        testState = ShadowState(
            reported={"Color": "Red"},
            desired=None,
            desired_is_nullable=True
        )

        self.assertEqual(testState.to_payload(), {"reported": {"Color": "Red"}, "desired": None})

    def test_shadow_state_payload_from_payload_null(self):
        expected_state = ShadowState.from_payload({"reported": {"deviceAgent": {"rebootRequired": True}}})
        assert {"reported": {"deviceAgent": {"rebootRequired": True}}} == expected_state.to_payload()
