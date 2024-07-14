from datetime import datetime
import logging

class Logger:
    def __init__(self, logger: logging) -> None:
        self._logger = logger
    
    def info(self, val: str):
        self._logger.info(f"[{datetime.now()}] {val}")
