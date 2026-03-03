class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:dbconnect725!@localhost/mechanic_shop'
    DEBUG = True
    CACHE_DEFAULT_TIMEOUT = 300 # after 5 minutes cache will refresh


class TestingConfig:
    pass


class ProductionConfig:
    pass 