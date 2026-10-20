from flask import request

from security.brasil_ip import ValidarIP

def configurar_waf(app):
    Validar_ip = ValidarIP()

    @app.before_request
    def verificar_ip():
        ip = request.remote_addr

        if not ip:
            return "IP não identificado.", 403

        if not Validar_ip.ip_autorizado(ip):
            app.logger.warning("IP bloqueado: %s | rota=%s | metodo=%s",
              ip,
              request.path,
              request.method
            )

            return "acesso não autorizado", 403

        app.logger.info("ip autorizado: %s | rota=%s",
          ip,
          request.path
        )