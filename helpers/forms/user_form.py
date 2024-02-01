from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from helpers.forms.validators.password_validators import (
    validate_senha_caracteres_especiais,
    validate_senha_maiusculas,
    validate_senha_minusculas,
    validate_senha_numeros,
    validate_senha_tamanho_minimo,
)


class FormularioUser(FlaskForm):
    nickname = StringField("Nickname", [DataRequired(), Length(min=1, max=8)])

    nome = StringField("Nome", [DataRequired(), Length(min=1, max=8)])

    senha = PasswordField(
        "Senha",
        validators=[
            validate_senha_tamanho_minimo,
            validate_senha_maiusculas,
            validate_senha_minusculas,
            validate_senha_numeros,
            validate_senha_caracteres_especiais,
        ],
    )
    salvar = SubmitField("Salvar")
