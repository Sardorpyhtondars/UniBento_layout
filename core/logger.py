import logging
import os

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    level=logging.WARNING,
    filename="logs/app.log",
    filemode="a",
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

logger_app: logging.Logger = logging.getLogger(__name__)