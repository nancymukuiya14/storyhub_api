import os
class Config:

    '''
    General configuration parent class
    
    '''
    
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:nancy@localhost/blogapp2'


class ProdConfig(Config):

    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True



config_options = {

    'development':DevConfig,
    'production':ProdConfig,
} 