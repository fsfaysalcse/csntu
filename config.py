class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/csndb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
