from dotenv import load_dotenv
from os import getenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

# Fake database (replace with real DB integration later)
fake_users_db = {
    "creator09": {
        "username": "creator0",
        "full_name": "Leonardo Nifinluri",
        "email": "leocode",
        # plain_password is 'secret'
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$WY/WsRWFC7jAeSYhAYiZ6Q$J5qITZCf6nz2r/XrLoe2dv2YmcqD3JLMx7yFfEoml5Y",
        "disabled": False,
    },
}

DATABASE_URL = getenv('DATABASE_URL')