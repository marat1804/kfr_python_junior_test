class Config:
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = 'Super super secret key'
