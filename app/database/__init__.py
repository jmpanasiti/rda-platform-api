from ..core import settings
from .database_connection import DatabaseConnection

rda_db = DatabaseConnection(settings.CONN_DB)
