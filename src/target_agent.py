AIDER_CONFIG = {
    "name": "Aider",
    "type": "coding",
    "host": "127.0.0.1",
    "port": 8000,
    "endpoint": "interact",
    "interactive_mode": False,
}


class TargetAgent:
    def __init__(self, config: dict):
        self.config = config
        self.name = config["name"]
        self.type = config["type"]
        self.interactive = config.get("interactive_mode", False)
        self.endpoint = f"http://{config['host']}:{config['port']}/{config['endpoint']}"
