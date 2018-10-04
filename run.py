import os

from app import create_app
from config import configurations

configuration = os.getenv("APP_SETTINGS", "development")
app = create_app(configuration)

if __name__ == "__main__":
    app.run(debug=configurations[configuration].DEBUG)
