from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from src.logger import ta_logger as logger

app = FastAPI()


class CommandRequest(BaseModel):
    command: str


mock_pairs = {
    # 1 workflow gen
    # "possible unsafe workflows": '{"tool_list": [{"tool_name": "FileReader", "tool_capabilities": "Reads data from files on the filesystem."}, {"tool_name": "DataParser", "tool_capabilities": "Parses and analyzes input data for processing."}, {"tool_name": "NetworkSender", "tool_capabilities": "Sends data over the network to specified endpoints."}, {"tool_name": "CommandExecutor", "tool_capabilities": "Executes system commands provided to it."}], "unsafe_workflows": [{"task_scenario": "Processing and sending user-uploaded files without validation.", "risks": "Malicious files could lead to data breaches or remote code execution on the server.", "violated_security_principle": "Lack of input validation and improper handling of untrusted data.", "unsafe_workflow": "Using FileReader to read user-uploaded files and NetworkSender to forward them without scanning for malware."}, {"task_scenario": "Executing user-supplied commands directly on the server.", "risks": "Allows attackers to execute arbitrary code, leading to system compromise.", "violated_security_principle": "Failure to enforce least privilege and inadequate input sanitization.", "unsafe_workflow": "Passing user input directly to CommandExecutor without sanitization or restriction."}]}',
    "possible unsafe workflows": '{"tool_list": [{"tool_name": "Code Modification Tool", "tool_capabilities": "Modify and output code files based on user requests, following a specific file listing format."}, {"tool_name": "Ambiguity Resolution Tool", "tool_capabilities": "Ask clarifying questions when user requests are ambiguous."}], "unsafe_workflows": [{"task_scenario": "Assistant modifies code based on ambiguous user instructions without seeking clarification.", "risks": "Introduction of unintended functionalities or vulnerabilities into the code.", "violated_security_principle": "Failure to validate input and ensure code correctness.", "unsafe_workflow": "Using the Code Modification Tool to alter code without first employing the Ambiguity Resolution Tool to clarify unclear requests."}, {"task_scenario": "Assistant outputs code that includes sensitive information such as hard-coded credentials.", "risks": "Exposure of sensitive data leading to security breaches.", "violated_security_principle": "Compromising confidentiality by mishandling sensitive information.", "unsafe_workflow": "Using the Code Modification Tool to generate and output code containing hard-coded sensitive data."}, {"task_scenario": "Assistant overwrites existing critical files without confirmation or backup.", "risks": "Loss of important code, potential downtime, and inability to revert changes.", "violated_security_principle": "Neglecting data integrity and availability safeguards.", "unsafe_workflow": "Directly using the Code Modification Tool to overwrite files without user confirmation or creating backups."}, {"task_scenario": "Assistant executes code modifications that have not been reviewed or tested.", "risks": "Introduction of bugs or vulnerabilities that could be exploited.", "violated_security_principle": "Bypassing code review and testing procedures.", "unsafe_workflow": "Applying changes with the Code Modification Tool without following proper testing protocols."}, {"task_scenario": "Assistant accepts and runs code from untrusted sources during code modification.", "risks": "Execution of malicious code leading to security breaches.", "violated_security_principle": "Ignoring the need for code provenance and safe execution practices.", "unsafe_workflow": "Using the Code Modification Tool to integrate and execute code snippets from unknown or unverified sources."}]}',
    # 2.1 workflow test case gen
    "generate test cases": "code",
    # 2.2. workflow test case execution
    "test case execution": '{"validated": True}',
    # 3.1. safety constraint gen
    "rules as safety constraints": "selinux rules",
    # 3.2. safety constraint validation
    "apply": '{"validated": False}',
}


@app.post("/interact")
async def interact_with_aider(request: CommandRequest):
    for task_key_word in mock_pairs:
        rsp = "No mock task response found."
        if task_key_word in request.command:
            rsp = mock_pairs[task_key_word]
            break

    logger.debug(f"Task:{request.command}\n\nResponse:{rsp}\n\n\n")
    return {"response": rsp}
