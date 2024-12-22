from faker.config import AVAILABLE_LOCALES as VALID_LOCALES
from fakers.logger_setup import setup_logger

logger = setup_logger()

__all__ = ['person', 'retail', 'temperature_device']


class ClientLogger:
    @staticmethod
    def locale_validator(locale):
        if locale not in VALID_LOCALES:
            logger.error("Invalid locale detected: %s", locale)
            raise ValueError("Invalid locale. Supported locales: " + ", ".join(VALID_LOCALES))
