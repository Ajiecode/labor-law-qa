import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, ChatHistory, QuestionStat
from extensions import db

bp = Blueprint('admin', __name__)

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403
    
    total_users = User.query.count()
    total_chats = ChatHistory.query.count()
    today_chats = ChatHistory.query.filter(
        db.func.date(ChatHistory.created_at) == db.func.date('now')
    ).count()
    
    top_questions = QuestionStat.query.order_by(QuestionStat.count.desc()).limit(10).all()
    
    return jsonify({
        'total_users': total_users,
        'total_chats': total_chats,
        'today_chats': today_chats,
        'top_questions': [{
            'question': q.question_text,
            'count': q.count
        } for q in top_questions]
    }), 200

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403
    
    users = User.query.all()
    
    return jsonify({
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'created_at': u.created_at.isoformat()
        } for u in users]
    }), 200
