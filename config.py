import os


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "superscret")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)


class Development(Config):
    DEBUG = True
    ENV = "development"
    DB_NAME = os.getenv("DB_FAST_FOOD_TEST", "testdb")


class Production(Config):
    DEBUG = False
    ENV = "production"
    DB_NAME = os.getenv("DB_FAST_FOOD", "fast_food")


class Testing(Config):
    DEBUG = True
    ENV = "testing"
    DB_NAME = os.getenv("DB_FAST_FOOD_TEST", "testdb")


configurations = {
    "development": Development,
    "production": Production,
    "testing": Testing
}
