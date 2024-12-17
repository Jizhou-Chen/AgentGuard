import unittest
import json
from src.agentGuard import AgentGuard, TargetAgent, AIDER_CONFIG


class TestGenRspToAgent(unittest.TestCase):
    def setUp(self):
        target_agent = TargetAgent(config=AIDER_CONFIG)
        self.agent_guard = AgentGuard(target_agent=target_agent)

    def test_gen_rsp_to_agent_confirmation(self):
        agent_msg = "Do you confirm the action?"
        expected_response = {
            "is_request": True,
            "command": "Y",
            "justification": "Confirmation requested.",
        }
        response = self.agent_guard._gen_rsp_to_agent(agent_msg)
        self.assertEqual(response, expected_response)

    def test_gen_rsp_to_agent_add_file(self):
        agent_msg = "Please add a new file named test.py."
        expected_response = {
            "is_request": True,
            "command": "/add test.py",
            "justification": "File creation requested.",
        }
        response = self.agent_guard._gen_rsp_to_agent(agent_msg)
        self.assertEqual(response, expected_response)

    def test_gen_rsp_to_agent_no_action(self):
        agent_msg = "Just a regular message with no action."
        expected_response = {
            "is_request": False,
            "command": "",
            "justification": "No action required.",
        }
        response = self.agent_guard._gen_rsp_to_agent(agent_msg)
        self.assertEqual(response, expected_response)


if __name__ == "__main__":
    unittest.main()
