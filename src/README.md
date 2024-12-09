
### Interact with Langflow agents
To interact with Langflow agents, separate chat sessions with session id (the corresponding session will be created if not already exists). For example,

```
curl -X POST \
    "http://127.0.0.1:7860/api/v1/run/f01cb878-cb94-4055-a59f-afb084998ed8?stream=false" \
    -H 'Content-Type: application/json'\
    -d '{"input_value": "can you compute 123*100 with python",
    "output_type": "chat",
    "input_type": "chat",
    "session_id": "JZC_SE",
    "tweaks": {
  "Agent-s7il1": {},
  "ChatInput-TfAGX": {},
  "ChatOutput-sLVxX": {},
  "URL-4eWno": {},
  "CalculatorTool-gXHMg": {},
  "PythonREPLTool-SQ0Rh": {}
}}
```