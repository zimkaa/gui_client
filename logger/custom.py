from __future__ import annotations
import json
import logging
import time


LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}

GREEN = "\x1b[38;5;40m"
RED = "\x1b[38;5;196m"
ORANGE = "\x1b[38;5;202m"
YELLOW = "\x1b[38;5;226m"
BLUE = "\x1b[38;5;21m"
NC = "\x1b[0m"

DATEFMT = "%Y-%m-%dT%H:%M:%S%z"


class StdoutCustomFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ) -> None:
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

        self.format_date = self.fmt_keys.get("datefmt", None)
        if self.format_date is None:
            self.format_date = DATEFMT

        format_string = self.fmt_keys.get("format", None)
        if format_string is None:
            format_string = "%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)3d | %(message)s"
        fmt = format_string.split(" | ")
        asctime = fmt[0]
        levelname = fmt[1]
        third_part = "".join(fmt[2:-1])
        message = fmt[-1]
        self.FORMATS = {
            logging.DEBUG: f"{GREEN}{asctime}{NC} | {levelname} | {third_part} | {message}",
            logging.INFO: f"{GREEN}{asctime}{NC} | {BLUE}{levelname} | {third_part}{NC} | {message}",
            logging.WARNING: f"{GREEN}{asctime}{NC} | {YELLOW}{levelname} | {third_part}{NC} | {message}",
            logging.ERROR: f"{GREEN}{asctime}{NC} | {ORANGE}{levelname} | {third_part}{NC} | {message}",
            logging.CRITICAL: f"{GREEN}{asctime}{NC} | {RED}{levelname} | {third_part}{NC} | {message}",
        }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.format_date)
        return formatter.format(record)


class JSONCustomFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ) -> None:
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord) -> dict[str, str]:
        ct = self.converter(record.created)
        timestamp = time.strftime(DATEFMT, ct)
        always_fields = {
            "message": record.getMessage(),
            "timestamp": timestamp,
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val if (msg_val := always_fields.pop(val, None)) is not None else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }

        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message
