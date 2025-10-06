from src.helpers.config import Settings, get_settings

class BaseDataModel:
    """
    Base class for all data models in the application.

    This class provides a shared interface for accessing
    the database client and application settings across all models.

    Attributes:
        db_client (object): The database client instance used to interact with the database.
        app_settings (Settings): Application configuration settings loaded from environment or config files.
    """

    def __init__(self, db_client:object) -> None:
        """
        Initialize the BaseDataModel with a database client.

        Args:
            db_client (object): SQLAlchemy database client or async session factory.
        """

        self.db_client = db_client
        self.app_settings = get_settings()
