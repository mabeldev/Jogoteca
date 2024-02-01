from flask import (
    Flask,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views.views_jogos import *
from views.views_user import *

if __name__ == "__main__":
    app.run(debug=True)
