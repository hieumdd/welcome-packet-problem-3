import sys

from logger import get_logger
from job.job import create_batch_operation

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        create_batch_operation()
        sys.exit(0)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
