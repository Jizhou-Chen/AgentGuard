from fastapi import FastAPI, HTTPException
from subprocess import Popen, PIPE
from contextlib import asynccontextmanager
from pydantic import BaseModel
import sys
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from src.logger import ta_logger as logger

app = FastAPI()

aider_process = None


def wait_for_prompt(line):
    return line[:-1].strip().endswith((">", "]:"))


def is_response(line):
    return "->" in line or (
        "─────────" not in line
        and "Tokens:" not in line
        and ">" != line.strip()
        and not line.strip().startswith("> ")
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    global aider_process
    try:
        aider_process = Popen(
            # ["aider", "--model=gpt-4o-mini", "--yes"],
            ["aider", "--model=gpt-4o", "--yes"],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=1,
        )
        while True:
            line = aider_process.stdout.readline()
            logger.debug(f"Aider: {line}")
            if wait_for_prompt(line):
                logger.debug("[Waiting for user input...]")
                break
        logger.debug("Aider process started.")
        yield
    finally:
        if aider_process:
            aider_process.terminate()
            logger.debug("Aider process terminated.")


app.router.lifespan_context = lifespan


class CommandRequest(BaseModel):
    command: str


def extract_json(text):
    """Extract valid JSON from text input.

    Args:
        text (str): Input text containing JSON

    Returns:
        dict: Extracted JSON as dictionary or None if invalid
    """
    try:
        # Find content between first { and last }
        json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
        matches = re.findall(json_pattern, text, re.DOTALL)

        if not matches:
            return None

        # Get the longest match as it's likely the complete JSON
        json_str = max(matches, key=len)

        # Clean up common issues
        json_str = json_str.strip()
        json_str = re.sub(r"[\r\n\t]", "", json_str)
        json_str = re.sub(r"\s+", " ", json_str)

        # Parse JSON
        result = json_str

        return result

    except (json.JSONDecodeError, ValueError):
        return None


@app.post("/interact")
async def interact_with_aider(request: CommandRequest):
    global aider_process
    if not aider_process:
        raise HTTPException(status_code=500, detail="Aider process is not running.")

    try:
        aider_process.stdin.write(f"{request.command}\n")
        aider_process.stdin.flush()

        output = []
        while True:
            line = aider_process.stdout.readline()
            # logger.debug(f"ALL:{repr(line)}")
            if line.strip() and line != "\n":
                if is_response(line):
                    logger.debug(f"Return: {line}")
                    output.append(line.strip())

            if wait_for_prompt(line):
                logger.debug("[Waiting for user input...]")
                break

        response = "\n".join(output)
        # Clean response for JSON responses
        if request.command and "{" in response and "}" in response:
            response = extract_json(response)
            logger.debug(f"Task:{request.command}\n\nResponse:{response}\n\n\n")
        return {"response": response}
    except Exception as e:
        logger.debug(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error interacting with aider: {e}"
        )
