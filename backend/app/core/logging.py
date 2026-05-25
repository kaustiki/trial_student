import logging
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parents[2] / "logs" / "app.log"
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)
    root_logger = logging.getLogger()
    # Show INFO and above. hided DEBUG
    root_logger.setLevel(logging.INFO)

    if not any(handler.get_name() == "student-care-console" for handler in root_logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.set_name("student-care-console")
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if not any(handler.get_name() == "student-care-file" for handler in root_logger.handlers):
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.set_name("student-care-file")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
