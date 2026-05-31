import logging
from logging.handlers import RotatingFileHandler
def log_set_up():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d — %(message)s",
        handlers=[
            RotatingFileHandler(
                "bot.logs",
                maxBytes=5 * 1024 * 1024,  #5 MB max
                backupCount=3,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = log_set_up()
