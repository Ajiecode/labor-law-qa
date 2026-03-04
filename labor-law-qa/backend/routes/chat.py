import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from models import ChatHistory, QuestionStat
from extensions import db
from datetime import datetime

bp = Blueprint('chat', __name__)

DIFY_API_URL = 'https://api.dify.ai/v1'
DIFY_API_KEY = ''  # 在部署时设置

@bp.route('/ask', methods=['POST'])
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
            headers={
                'Authorization': f'Bearer {DIFY_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'inputs': {'query': question},
                'response_mode': 'blocking',
                'user': f'user_{user_id}'
            },
            timeout=60
        )
        
        result = response.json()
        
        answer = ''
        if result.get('data') and result['data'].get('outputs'):
            answer = result['data']['outputs'].get('answer', '')
        
        history = ChatHistory(
            user_id=user_id,
            question=question,
            answer=answer,
            created_at=datetime.utcnow()
        )
        db.session.add(history)
        
        stat = QuestionStat.query.filter_by(question_text=question).first()
        if stat:
            stat.count += 1
        else:
            stat = QuestionStat(question_text=question, count=1)
            db.session.add(stat)
        
        db.session.commit()
        
        return jsonify({
            'answer': answer,
            'question': question
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'请求失败: {str(e)}'}), 500

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = ChatHistory.query.filter_by(user_id=user_id)\
        .order_by(ChatHistory.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'history': [{
            'id': h.id,
            'question': h.question,
            'answer': h.answer[:100] + '...' if len(h.answer) > 100 else h.answer,
            'created_at': h.created_at.isoformat()
        } for h in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    favorites = ChatHistory.query.filter_by(user_id=user_id, is_favorite=True)\
        .order_by(ChatHistory.created_at.desc()).all()
    
    return jsonify({
        'favorites': [{
            'id': f.id,
            'question': f.question,
            'answer': f.answer,
            'created_at': f.created_at.isoformat()
        } for f in favorites]
    }), 200

@bp.route('/favorite/<int:history_id>', methods=['POST'])
@jwt_required()
def toggle_favorite(history_id):
    user_id = get_jwt_identity()
    history = ChatHistory.query.filter_by(id=history_id, user_id=user_id).first()
    
    if not history:
        return jsonify({'message': '记录不存在'}), 404
    
    history.is_favorite = not history.is_favorite
    db.session.commit()
    
    return jsonify({
        'is_favorite': history.is_favorite
    }), 200
