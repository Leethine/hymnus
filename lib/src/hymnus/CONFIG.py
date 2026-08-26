SQLITE_MAX_RETRY = 10
SQLITE_WAIT_TIME = 0.5

DB_SYSTEM = "SQLite3"
DB_PATH   = "/home/hymnus/hymnus.db"
# Filesystem directory
FS_PATH   = "/home/hymnus/hymnus_fs"
# User name and password directory
USER_PATH = "/home/hymnus/hymnus_users"

COMPOSERS_PER_PAGE   = 15
COLLECTIONS_PER_PAGE = 10
PIECES_PER_PAGE      = 10

# Manually-set wait time to protect the web application
FILE_UPLOAD_WAIT_TIME   = 0.5
FILE_DOWNLOAD_WAIT_TIME = 0.5

# Allowed file extensions
ACCEPTED_FILE_UPLOAD_EXTENSIONS = \
['.pdf', '.xml', '.mxl', '.musicxml', '.ly', '.mid', '.midi', \
 '.txt', '.zip', '.eps', '.png', '.tex']
