from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import requests
import json
import time
import uvicorn
import subprocess

TARGET_AGENT_SERVER_CONFIG = {"host": "127.0.0.1", "port": 8000, "endpoint": "interact"}


class TargetAgent:
    def __init__(self, config: dict, name: str, type: str):
        self.config = config
        self.name = name
        self.type = type
        self.endpoint = f"http://{config['host']}:{config['port']}/{config['endpoint']}"


class AgentGuard:
    def __init__(self, target_agent: TargetAgent, llm=None):
        self.target_agent = target_agent
        self.llm = ChatOpenAI(model_name="gpt-4") if not llm else llm

    def instruct(self, task: str) -> dict:
        instruction = self._gen_instruction(task)
        msg = {"command": instruction}
        return self._send(msg)

    def respond(self, context: str) -> dict:
        response = self._gen_response(context)
        msg = {"command": choice}
        return self._send(msg)

    def _send(self, msg: dict) -> dict:
        print(f"Querying target agent with: {msg}")
        response = requests.post(self.target_agent_endpoint, json=msg)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.status_code} {response.text}")

    def _gen_instruction(self, task: str):
        msgs = [self.sys_msg_instruct, HumanMessage(content=task)]
        instruction = self.llm.invoke(msgs).content
        return instruction

    def _gen_response(self, context: str):
        msgs = [self.sys_msg_respond, HumanMessage(content=context)]
        instruction = self.llm.invoke(msgs).content
        return instruction


if __name__ == "__main__":
    target_agent = TargetAgent(
        config=TARGET_AGENT_SERVER_CONFIG, name="Aider", type="coding"
    )
    agent_guard = AgentGuard(target_agent_endpoint=target_agent.endpoint)

    # Test query
    user_prompt = "Generate a prompt to let Aider write a Python code to solve a simple math problem as if you are directly interacting with Aider"
    print(agent_guard.instruct(user_prompt=user_prompt))

    # Test confirmation
    # TODO: ask ag to generate confirmation automatically
    choice = "Y"
    print(agent_guard.respond(choice="y"))

    # print("Identifying risky workflows...")
    # risky_workflows = agent_guard.identify_risky_workflows()
    # print("Risky Workflows Identified:", risky_workflows)

    # exit()

    # print("Validating risky workflows...")
    # validated_risks = agent_guard.validate_risky_workflows(risky_workflows)
    # print("Validated Risks:", validated_risks)

    # print("Generating sandbox policies...")
    # sandbox_policies = agent_guard.generate_sandbox_policies(validated_risks)
    # print("Sandbox Policies Generated:", sandbox_policies)

    # print("Validating sandbox policies...")
    # policy_validation_results = agent_guard.validate_sandbox_policies(sandbox_policies)
    # print("Policy Validation Results:", policy_validation_results)

    # print("Evaluating safety metrics...")
    # metrics = agent_guard.evaluate_safety_metrics(
    #     validated_risks, policy_validation_results
    # )
    # print("Safety Metrics:", metrics)
