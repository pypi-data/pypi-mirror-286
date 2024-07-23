
import logging


def get_logger(name: str, debug: bool = False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.WARNING)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s[%(name)s] : %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False  # Отключение распространения логов вверх по иерархии
    return logger