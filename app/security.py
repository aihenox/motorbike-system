import hmac
import secrets

from functools import wraps

from flask import abort, jsonify, request, session

from flask_login import current_user


SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}


def admin_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if getattr(current_user, "rol", None) != "Administrador":

            abort(403)

        return view(*args, **kwargs)

    return wrapped


def generar_token_csrf():

    token = session.get("_csrf_token")

    if not token:

        token = secrets.token_urlsafe(32)

        session["_csrf_token"] = token

    return token


def init_security(app):

    @app.context_processor
    def csrf_context():

        return {
            "csrf_token": generar_token_csrf
        }

    @app.before_request
    def validar_csrf():

        if request.method in SAFE_METHODS:

            return None

        esperado = session.get("_csrf_token")

        recibido = (
            request.headers.get("X-CSRF-Token")
            or request.form.get("_csrf_token")
        )

        if (
            not esperado
            or not recibido
            or not hmac.compare_digest(esperado, recibido)
        ):

            return jsonify({
                "success": False,
                "message": "Solicitud inválida o sesión vencida. Recargue la página."
            }), 400

        return None

    @app.after_request
    def agregar_cabeceras_seguridad(response):

        response.headers.setdefault(
            "X-Content-Type-Options",
            "nosniff"
        )

        response.headers.setdefault(
            "X-Frame-Options",
            "SAMEORIGIN"
        )

        response.headers.setdefault(
            "Referrer-Policy",
            "strict-origin-when-cross-origin"
        )

        return response
