from wtforms import ValidationError


def validate_senha_tamanho_minimo(self, senha):
    if len(senha.data) < 8:
        raise ValidationError("A senha deve ter no mínimo 8 caracteres.")


def validate_senha_maiusculas(self, senha):
    if not any(char.isupper() for char in senha.data):
        raise ValidationError("A senha deve conter letras maiúsculas.")


def validate_senha_minusculas(self, senha):
    if not any(char.islower() for char in senha.data):
        raise ValidationError("A senha deve conter letras minúsculas.")


def validate_senha_numeros(self, senha):
    if not any(char.isdigit() for char in senha.data):
        raise ValidationError("A senha deve conter números.")


def validate_senha_caracteres_especiais(self, senha):
    if not any(not char.isalnum() for char in senha.data):
        raise ValidationError("A senha deve conter caracteres especiais.")
