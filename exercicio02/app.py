from controllers.html_basico_controller import HTMLbasicocontroller
from flask import Flask
from controllers.login_controller import LoginController

app = Flask(__name__)

LoginController(app)
HTMLbasicocontroller(app)

app.secret_key = "log_ex02"

if __name__ == "__main__":
    app.run(debug=True)