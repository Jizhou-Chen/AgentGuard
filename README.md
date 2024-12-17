# AgentAguard
### Setup Environment

1. **Create a virtual environment**:
    ```sh
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Start Aider
```
mkdir util/workdir && cd util/workdir
git init # required by Aider
uvicorn aider_server:app --app-dir .. # Do not use --reload as it may restart the session
```
### Start AgentGuard
To run AgentGuard, execute the following
```
python3 -m src.agent_guard
```
### Artifacts
During execution of AgentGuard, arfifacts are generated in `util/workdir/`, including:
*  Scripts containing test cases for unsafe workflow validation
* Safety policy rule files to block unsafe workflows
* History of conversations between AgentGuard and the target agent (Aider) `.aider.chat.history.md`.