from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import check_password_hash, generate_password_hash

from helpers.forms.login_form import FormularioLogin
from helpers.forms.user_form import FormularioUser
from jogoteca import app, db
from models.models import Usuarios


@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    form = FormularioLogin()
    return render_template(
        "User/login.html", titulo="Login", proxima=proxima, form=form
    )


@app.route("/autenticar", methods=["POST"])
def autenticar():
    proxima_pagina = request.form.get("proxima")
    form = FormularioLogin(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = form.senha.data

    if usuario and check_password_hash(usuario.senha, senha):
        session["usuario"] = usuario.nickname
        flash(session["usuario"] + " Logado com sucesso!", "success")
        return (
            redirect(proxima_pagina)
            if proxima_pagina
            else redirect(url_for("index"))
        )
    flash("Usuário ou senha inválidos!", "danger")
    return (
        redirect(url_for("login", proxima=proxima_pagina))
        if proxima_pagina
        else redirect(url_for("login"))
    )


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Usuário deslogado!", "info")
    return redirect(url_for("index"))


@app.route("/novo_usuario")
def novo_usuario():
    form = FormularioUser()
    return render_template(
        "User/novo_usuario.html", titulo="Novo Usuário", form=form
    )


@app.route("/criar_usuario", methods=["POST"])
def criar_usuario():
    form = FormularioUser(request.form)
    errors = ""
    if not form.validate_on_submit():
        for field_name, field_errors in form.errors.items():
            for error in field_errors:
                errors += error + "\n"
        flash(f"Erro ao cadastrar novo usuário! {errors}", "danger")
        return redirect(url_for("novo_usuario"))
    nome = form.nome.data
    nickname = form.nickname.data
    senha = generate_password_hash(form.senha.data)
    user = Usuarios.query.filter_by(nickname=nickname).first()
    if user:
        flash("Usuário já existe!", "danger")
        return redirect(url_for("novo_usuario"))
    user = Usuarios(nome, nickname, senha)
    db.session.add(user)
    db.session.commit()
    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for("index"))
