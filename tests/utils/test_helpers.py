import logging

from app.core import settings
from app.database import DatabaseConnection


def get_logger(name: str = 'test_logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('./tests/test.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_db_test():
    db_test = DatabaseConnection(settings.CONN_DB_TEST)

    return db_test


def is_db_test_present() -> bool:
    db = get_db_test()

    if db.connect():
        get_logger().info('db_test connection OK')
        db.disconnect()
        return True

    get_logger().error('db_test connection FAIL')
    return False


skip_db_test = not is_db_test_present()
