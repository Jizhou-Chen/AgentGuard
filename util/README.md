### Interact with Aider remotely
* Server side: `uvicorn remote_aider:app --reload`
    * Requires Aider installed
* Client side: `curl -X POST "http://127.0.0.1:8000/interact" -H "Content-Type: application/json" -d '{"command": "USER PROMPT"}'`
    * TODO: incoporate into Agent Guard agent