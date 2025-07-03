import logging
from datetime import datetime
import os

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = f"logs/test_log_{timestamp}.log"
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=log_path,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger()
