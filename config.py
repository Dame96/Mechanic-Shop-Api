class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:dbconnect725!@localhost/mechanic_shop'
    DEBUG = True


class TestingConfig:
    pass


class ProductionConfig:
    pass 