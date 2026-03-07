from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}}, supports_credentials=True)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'labor-law-qa-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///labor_law.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'labor-law-jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@app.route('/api/auth/profile', methods=['GET', 'OPTIONS'])
@app.route('/api/chat/ask', methods=['POST', 'OPTIONS'])
@app.route('/api/chat/history', methods=['GET', 'OPTIONS'])
@app.route('/api/chat/favorites', methods=['GET', 'OPTIONS'])
@app.route('/api/admin/stats', methods=['GET', 'OPTIONS'])
def cors_preflight():
    return '', 200

from routes.auth import bp as auth_bp
from routes.chat import bp as chat_bp
from routes.admin import bp as admin_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
