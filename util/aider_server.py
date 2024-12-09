from fastapi import FastAPI, HTTPException
from subprocess import Popen, PIPE
from contextlib import asynccontextmanager
from pydantic import BaseModel

app = FastAPI()

aider_process = None


def wait_for_prompt(line):
    return line[:-1].strip().endswith((">", "]:"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    global aider_process
    try:
        aider_process = Popen(
            ["aider"],  # Test with a valid aider command
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=1,
        )
        while True:
            line = aider_process.stdout.readline()
            # print(f"ALL:{repr(line)}")
            if wait_for_prompt(line):
                print(line)
                break
        print("Aider process started.")
        yield
    finally:
        if aider_process:
            aider_process.terminate()
            print("Aider process terminated.")


app.router.lifespan_context = lifespan


class CommandRequest(BaseModel):
    command: str


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
            # print(f"ALL:{repr(line)}")
            if line.strip() and line != "\n":
                print(f"Aider: {line}")
                output.append(line.strip())

            if wait_for_prompt(line):
                print("[Waiting for user input...]")
                break

        return {"response": "\n".join(output)}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error interacting with aider: {e}"
        )


@app.get("/debug")
async def debug():
    global aider_process
    if aider_process:
        stderr_output = aider_process.stderr.read()
        return {"stderr": stderr_output}
    return {"message": "Aider process is not running."}
