from flask import (
    render_template,
    jsonify,
    request
)

from werkzeug.exceptions import HTTPException


# ==========================================
# REGISTRAR ERRORES
# ==========================================
def register_error_handlers(app):


    # ==========================================
    # ERROR 403
    # ==========================================
    @app.errorhandler(403)
    def forbidden(error):

        if request.path.startswith("/api"):

            return jsonify({
                "success": False,
                "message": "No tiene permisos para realizar esta acción"
            }), 403

        return render_template(
            "errors/403.html"
        ), 403


    # ==========================================
    # ERROR 404
    # ==========================================
    @app.errorhandler(404)
    def not_found(error):

        if request.path.startswith("/api"):

            return jsonify({

                "success": False,

                "message": "Ruta no encontrada"

            }), 404

        return render_template(
            "errors/404.html"
        ), 404


    # ==========================================
    # ERROR 500
    # ==========================================
    @app.errorhandler(500)
    def internal_error(error):

        if request.path.startswith("/api"):

            return jsonify({

                "success": False,

                "message": "Error interno del servidor"

            }), 500

        return render_template(
            "errors/500.html"
        ), 500


    # ==========================================
    # ERROR GENERAL
    # ==========================================
    @app.errorhandler(Exception)
    def general_error(error):

        if isinstance(error, HTTPException):

            if request.path.startswith("/api"):

                return jsonify({
                    "success": False,
                    "message": error.description
                }), error.code

            return error

        app.logger.exception(
            "Error no controlado durante la solicitud",
            exc_info=error
        )

        if request.path.startswith("/api"):

            return jsonify({

                "success": False,

                "message": "Error interno del servidor"

            }), 500

        return render_template(
            "errors/500.html"
        ), 500
