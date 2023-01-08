class Config(object):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/bukh'
    # WTForsm
    # WTF_CSRF_SECRET_KEY = 'a random string'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'somesecretke123somesecretey'