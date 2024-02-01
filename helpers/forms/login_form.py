from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators


class FormularioLogin(FlaskForm):
    nickname = StringField(
        "Nickname",
        [
            validators.DataRequired(),
            validators.Length(min=1, max=8),
        ],
    )
    senha = PasswordField(
        "Senha",
        [
            validators.DataRequired(),
            validators.Length(min=1, max=100),
        ],
    )
    entrar = SubmitField("Entrar")
