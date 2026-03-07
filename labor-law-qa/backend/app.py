import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'labor-law-secret-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///labor_law.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'labor-law-jwt-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

db = SQLAlchemy(app)
jwt = JWTManager(app)

DIFY_API_URL = 'https://api.dify.ai/v1'
DIFY_API_KEY = os.environ.get('DIFY_API_KEY', '')

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

# Auth routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户名已存在'}), 400
    user = User(username=data['username'], email=data.get('email', ''))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': '用户名或密码错误'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user': {'id': user.id, 'username': user.username}
    })

# Chat routes
@app.route('/api/chat/ask', methods=['POST'])
@jwt_required()
def ask():
    user_id = get_jwt_identity()
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'message': '问题不能为空'}), 400
    
    try:
        response = requests.post(
            f'{DIFY_API_URL}/workflows/run',
            headers={'Authorization': f'Bearer {DIFY_API_KEY}', 'Content-Type': 'application/json'},
            json={'inputs': {'query': question}, 'response_mode': 'blocking', 'user': f'user_{user_id}'},
            timeout=60
        )
        result = response.json()
        answer = ''
        if result.get('data') and result['data'].get('outputs'):
            answer = result['data']['outputs'].get('answer', '')
        
        history = ChatHistory(user_id=user_id, question=question, answer=answer)
        db.session.add(history)
        db.session.commit()
        
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'message': f'请求失败: {str(e)}'}), 500

@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    history = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.id.desc()).limit(20).all()
    return jsonify({'history': [{'id': h.id, 'question': h.question, 'answer': h.answer[:100]} for h in history]})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
