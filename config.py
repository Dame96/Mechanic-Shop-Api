import os 

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:dbconnect725!@localhost/mechanic_shop'
    DEBUG = True
    CACHE_DEFAULT_TIMEOUT = 300 # after 5 minutes cache will refresh


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True 
    CACHE_TYPE = 'SimpleCache' 


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"