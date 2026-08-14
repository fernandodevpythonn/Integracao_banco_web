from flask import Flask
from controllers.html_basico_controller import HTMLbasicoController
from controllers.login_controller import LoginController
app = Flask(__name__)

HTMLbasicoController(app)
LoginController(app)
app.secret_key = "log_ex03"

if __name__ == "__main__":
    app.run(debug=True)

