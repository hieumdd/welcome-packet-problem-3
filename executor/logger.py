import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record_dict = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "filename": record.funcName,
            "funcName": record.funcName,
            "lineno": record.lineno,
            **(record.args if isinstance(record.args, dict) else {}),
        }
        return json.dumps(record_dict)


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(JsonFormatter())
    logger.addHandler(ch)
    return logger
