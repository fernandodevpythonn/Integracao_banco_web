from flask import Flask
from controllers.html_basicocontroller import htmlbasicocontroller
from controllers.logincontroller import LoginController

app = Flask(__name__)

app.secret_key = "log_ex01"

htmlbasicocontroller(app)
LoginController(app)

if __name__ == "__main__":
    app.run(debug=True)