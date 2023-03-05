class Config(object):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/bukh'
    # WTForsm
    # WTF_CSRF_SECRET_KEY = 'a random string'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'somesecretke123somesecretey'
    CORS_HEADERS = 'Content-Type'

token_dadata = "081ade560a703d3f76189f0c90cce85ccc44000f"
secret_datdata = "6f582c5b62ca9c9914aa215a3461f0a88d233865"