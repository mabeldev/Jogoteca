import time

from flask import (
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from helpers.forms.game_form import FormularioJogo
from helpers.helpers import (
    deleta_imagem,
    recupera_imagem,
)
from jogoteca import app, db
from models.models import Jogos

upload_path = app.config["UPLOAD_PATH"]


@app.route("/")
def index():
    jogos = Jogos.query.order_by(Jogos.id)
    return render_template(
        "Game/lista_jogos.html", titulo="Jogos", jogos=jogos
    )


@app.route("/novo")
def novo():
    if "usuario" not in session or session["usuario"] is None:
        flash("Faça login para acessar essa página!", "danger")
        return redirect(url_for("login", proxima=url_for("novo")))
    form = FormularioJogo()
    return render_template(
        "Game/novo_jogo.html", titulo="Novo Jogo", form=form
    )


@app.route("/criar", methods=["POST"])
def criar():
    form = FormularioJogo(request.form)
    if not form.validate_on_submit():
        flash("Erro ao cadastrar novo jogo!", "danger")
        return redirect(url_for("novo"))
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash("Jogo já existe!", "danger")
        return redirect(url_for("novo"))
    jogo = Jogos(nome, categoria, console)
    db.session.add(jogo)
    db.session.commit()

    image = request.files["image"]

    timestamp = time.time()
    image.save(f"{upload_path}/capa-{jogo.id}-{timestamp}.jpg")

    return redirect(url_for("index"))


@app.route("/editar/<int:id>")
def editar(id: int):
    if "usuario" not in session or session["usuario"] is None:
        flash("Faça login para acessar essa página!", "danger")
        return redirect(url_for("login", proxima=url_for("editar")))
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa = recupera_imagem(id)
    return render_template(
        "Game/editar_jogo.html",
        titulo="Editar Jogo",
        form=form,
        capa=capa,
        id=id,
    )


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id: int):
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo(request.form)
    if not form.validate_on_submit():
        flash("Erro ao atualizar jogo!", "danger")
        return redirect(url_for("index"))
    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data
    db.session.commit()

    image = request.files["image"]
    if image:
        timestamp = time.time()
        deleta_imagem(id)
        image.save(f"{upload_path}/capa-{jogo.id}-{timestamp}.jpg")

    flash("Jogo atualizado com sucesso!", "success")
    return redirect(url_for("index"))


@app.route("/deletar/<int:id>")
def deletar(id: int):
    if "usuario" not in session or session["usuario"] is None:
        flash("Faça login para acessar essa página!", "danger")
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    deleta_imagem(id)

    flash("Jogo deletado com sucesso!", "success")
    return redirect(url_for("index"))


@app.route("/uploads/<path:nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory(upload_path, nome_arquivo)
