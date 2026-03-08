from flask import Flask, jsonify
from config import Config
from extensions import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(transaction_bp, url_prefix="/api")

@app.route("/")
def home():
    return jsonify({"message": "Personal Finance Tracker API is running"})

if __name__ == "__main__":
    app.run(debug=True)