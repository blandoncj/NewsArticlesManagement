class Config:
    SECRET_KEY = "4gbt7KCnPyJy44VuoIe0lePvaFJZw0C3tEFX4WfEvNGkSYRPrwJjEjRI3bpPfniFkcHOKYGaArZFBmuX1PccJdUa9q8gDo8njh2o2QaP4MQu2SfGZpi6TksRcqShNlZl"


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "db_newspaper-analytic"


config = {"development": DevelopmentConfig}
