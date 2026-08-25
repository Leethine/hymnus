from metadata_sqlite import SQLiteReadMetadata
from metadata_sqlite import SQLiteWriteMetadata
from utilities import SingletonMeta
from config import DB_SYSTEM

class Metadata(metaclass=SingletonMeta):
  """ Intermediate metadata interface depending on the database system. """
  
  def reader(self):
    """Return metadata reader instance."""
    #if DB_SYSTEM == "sqlite":
    return SQLiteReadMetadata()
  
  def writer(self):
    """Return metadata writer instance."""
    #if DB_SYSTEM == "sqlite":
    return SQLiteWriteMetadata()
