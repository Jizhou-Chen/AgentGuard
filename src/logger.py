import logging

ag_logger = logging.getLogger("Debugger")
ag_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(name)s] %(message)s\n")
console_handler.setFormatter(formatter)
ag_logger.addHandler(console_handler)
