class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://zeka:zeka@localhost:5432/smart_home'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    port = 8000
    JWT_SECRET_KEY = '9543cfc2be73c2b1b016efe66e94c0448ea712938a2655db691d799bb6e2024b'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days