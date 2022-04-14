from pydoc import describe
from unittest import TestCase

from awsiot.iotshadow import ShadowState


class ShadowTest(TestCase):

    def test_shadow_state_payload_filled(self):
        test_state = ShadowState.from_payload({
            "reported": {"Color": "Red"},
            "desired": {"Color": "Blue"}
        })
        compareState = ShadowState(
            reported={"Color": "Red"},
            desired={"Color": "Blue"}
        )
        self.assertTrue(test_state.to_payload() == compareState.to_payload())

    def test_shadow_state_payload_partial_filled(self):
        test_state = ShadowState.from_payload({
            "reported": {"Color": "Red"}
        })
        self.assertEqual(test_state.to_payload(), {"reported": {"Color": "Red"}})

    def test_shadow_state_payload_can_send_null(self):
        test_state = ShadowState(
            reported={"Color": "Red"},
            desired=None,
            desired_is_nullable=True
        )
        self.assertEqual(test_state.to_payload(), {"reported": {"Color": "Red"}, "desired": None})

    def test_shadow_state_payload_with_none(self):
        test_state = ShadowState.from_payload({"reported": {"Color": "Red"}, "desired": None})
        self.assertTrue(test_state.desired_is_nullable)
        self.assertEqual(test_state.to_payload(), {"reported": {"Color": "Red"}, "desired": None})

    def test_shadow_state_payload_without_none(self):
        test_state = ShadowState.from_payload({"reported": {"deviceAgent": {"rebootRequired": True}}})
        self.assertEqual(test_state.to_payload(), {"reported": {"deviceAgent": {"rebootRequired": True}}})
