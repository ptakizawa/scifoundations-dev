import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SF_SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'peter.takizawa@gmail.com' #os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'Sj7WUHjpT32uC6J' #os.environ.get('MAIL_PASSWORD')
    SF_MAIL_SUBJECT_PREFIX = '[Scientific Foundations]'
    SF_MAIL_SENDER = 'Sci Foundations Admin <peter.takizawa@gmail.com>'
    SF_ADMIN = os.environ.get('SF_ADMIN')
    THREADS = ['biochemistry', 'cell-biology', 'epidemiology-and-public-health', 'genetics', 'embryology', 'pathology', 'pharmacology', 'physiology']
    THEMES = ['building-a-body', 'cell-communication', 'cell-energy', 'epidemiology-and-public-health', 'fluids-and-gradients', 'gene-expression', 'life-and-death-of-a-cell']
    BLOOMS_TAXONOMY = ['knowledge', 'comprehension', 'application', 'analysis', 'synthesis', 'evaluation']
    IMAGE_FOLDER = 'app/static/images/'
    ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://sf_admin:'+DATABASE_PASSWORD+'@localhost:5432/sf_dev'
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL') or 'postgresql://localhost:5432/sf_test'+DATABASE_PASSWORD+'@localhost:5432/sf_test'
    

class ProductionConfig(Config):
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://sf_admin:'+DATABASE_PASSWORD+'@localhost:5432/sf'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

