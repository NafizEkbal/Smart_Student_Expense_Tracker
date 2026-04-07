from flask import Flask
from routes.auth import auth
from routes.dashboard import dashboard

app = Flask(__name__)
app.secret_key="chabi"

app.register_blueprint(auth)
app.register_blueprint(dashboard)

if __name__ == '__main__':
    app.run(debug=True)