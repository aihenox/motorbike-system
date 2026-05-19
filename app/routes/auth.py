from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash
)

from flask_login import (

    login_user,

    logout_user,

    login_required
)

from app.services.auth_service import (

    User,

    validar_login
)


auth_bp = Blueprint(

    "auth",

    __name__
)


# ==========================================
# LOGIN
# ==========================================
@auth_bp.route(

    "/",

    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        usuario = request.form[
            "usuario"
        ]

        password = request.form[
            "password"
        ]

        user_db = validar_login(

            usuario,

            password
        )

        if user_db:

            user = User(
                user_db["id"]
            )

            login_user(user)

            return redirect(
                url_for(
                    "dashboard.dashboard"
                )
            )

        flash(
            "Usuario o contraseña incorrectos"
        )

    return render_template(
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )