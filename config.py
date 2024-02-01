import os

import dotenv

dotenv.load_dotenv()

SECRET_KEY = "minha_chave_secreta"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{user}:{senha}@{servidor}/{db}".format(
    SGBD="mysql+mysqlconnector",
    user=os.getenv("DB_USER"),
    senha=os.getenv("DB_PASSWORD"),
    servidor="localhost",
    db="jogoteca2",
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
