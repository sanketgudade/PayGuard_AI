from flask import Blueprint, request, jsonify
from ..services.ai_agent import analyze_transaction
from ..models.user import Policy

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    # In a real app, get user_id from auth token
    user_id = 1
    policy = Policy.query.filter_by(user_id=user_id).first()
    
    if not policy:
        return jsonify({"error": "Policy not found"}), 404
        
    analysis = analyze_transaction(data, policy)
    
    return jsonify(analysis)
