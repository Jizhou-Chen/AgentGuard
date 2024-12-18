import logging

ag_logger = logging.getLogger("AG Logger")
ag_logger.setLevel(logging.DEBUG)

ta_logger = logging.getLogger("TA Logger")
ta_logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s\n\n"))

ag_file_handler = logging.FileHandler("ag.log", mode="a")
ag_file_handler.setLevel(logging.DEBUG)
ag_file_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s\n\n"))

ta_file_handler = logging.FileHandler("ta.log", mode="a")
ta_file_handler.setLevel(logging.DEBUG)
ta_file_handler.setFormatter(logging.Formatter("[%(name)s] %(message)s\n\n"))

ag_logger.addHandler(console_handler)
ag_logger.addHandler(ag_file_handler)

ta_logger.addHandler(console_handler)
ta_logger.addHandler(ta_file_handler)
