import os
from app import create_app
from config import configurations
from app.db import database
configuration = os.getenv("APP_SETTINGS", "development")
app = create_app(configuration)
database.create_tables()
# print(DATABASE.connection)
if __name__ == "__main__":
    app.run(debug=configurations[configuration].DEBUG)