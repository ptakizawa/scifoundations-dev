import os
basedir = os.path.abspath('os.path.dirname(__file__)')

class Config:
    SECRET_KEY = os.environ.get('SF_SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SF_MAIL_SUBJECT_PREFIX = '[Scientific Foundations]'
    SF_MAIL_SENDER = 'Sci Foundations Admin <peter.takizawa@gmail.com>'
    SF_ADMIN = os.environ.get('SF_ADMIN')
    THREADS = ['biochemistry', 'cell-biology', 'epidemiology-and-public-health', 'genetics', 'embryology', 'pathology', 'pharmacology', 'physiology']
    THEMES = ['building-a-body', 'cell-communication', 'cell-energy', 'epidemiology-and-public-health', 'fluids-and-gradients', 'gene-expression', 'life-and-death-of-a-cell']
    BLOOMS_TAXONOMY = ['knowledge', 'comprehension', 'application', 'analysis', 'synthesis', 'evaluation']

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://sf_admin:etwbisf413@localhost:5432/sf_dev'
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL') or 'postgresql://localhost:5432/sf_test'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost:5432/sf'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

