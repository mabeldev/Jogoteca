import os

from jogoteca import app

upload_path = app.config["UPLOAD_PATH"]


def recupera_imagem(id: int):
    for nome_arquivo in os.listdir(upload_path):
        if f"capa-{id}" in nome_arquivo:
            return nome_arquivo
    return "padrao.png"


def deleta_imagem(id: int):
    imagem = recupera_imagem(id)
    if imagem != "padrao.png":
        os.remove(os.path.join(upload_path, imagem))
