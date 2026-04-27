from flask import Flask
from routes.auth import auth
from routes.dashboard import dashboard
from routes.transaction import transaction
from routes.profile import user_profile

app = Flask(__name__)
app.secret_key="chabi"

app.register_blueprint(auth)
app.register_blueprint(user_profile)
app.register_blueprint(dashboard)
app.register_blueprint(transaction)

if __name__ == '__main__':
    app.run(debug=True)

