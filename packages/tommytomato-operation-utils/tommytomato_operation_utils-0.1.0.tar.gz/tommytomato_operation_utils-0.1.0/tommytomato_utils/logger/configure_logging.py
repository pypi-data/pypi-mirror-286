import logging

from tommytomato_utils.logger.logger import Logger
from tommytomato_utils.logger.db_logging_handler import DatabaseLoggingHandler
from tommytomato_utils.database_client.database_client import DatabaseClient


def configure_logging(
        db_client: DatabaseClient = None,
        hub_id: str = None,
        run_id: str = None,
        user_id: str = None,
        tool_name: str = None,
        log_to_db: bool = False,
        log_level: int = logging.INFO
):
    """
    Configures the logging setup.

    Args:
        db_client (DatabaseClient): Database client for logging to the database.
        hub_id (str): Hub ID for logging.
        run_id (str): Run ID for logging.
        user_id (str): User ID for logging.
        tool_name (str): Tool name for logging.
        log_to_db (bool): Flag to enable logging to the database.
        log_level (int): Logging level.
    """
    custom_logger = Logger(level=log_level)
    logger_instance = custom_logger.get_logger()

    if log_to_db:
        if not all([db_client, hub_id, run_id, user_id, tool_name]):
            raise ValueError(
                "All database logging parameters must be provided when log_to_db is True")

        db_handler = DatabaseLoggingHandler(
            db_client=db_client,
            hub_id=hub_id,
            run_id=run_id,
            user_id=user_id,
            tool_name=tool_name
        )
        db_handler.setLevel(log_level)
        custom_logger.add_handler(db_handler)

    return custom_logger
