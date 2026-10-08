from flask import Blueprint, request, jsonify
from ..models import db
from ..models.user import Policy

policies_bp = Blueprint('policies', __name__)

@policies_bp.route('/', methods=['GET'])
def get_policies():
    user_id = 1 # mock auth
    policy = Policy.query.filter_by(user_id=user_id).first()
    if not policy:
        return jsonify({"error": "Not found"}), 404
        
    return jsonify({
        "autonomous_limit": float(policy.autonomous_limit),
        "daily_limit": float(policy.daily_limit),
        "monthly_limit": float(policy.monthly_limit),
        "new_merchant_approval": policy.new_merchant_approval,
        "high_risk_block": policy.high_risk_block
    })

@policies_bp.route('/', methods=['PUT'])
def update_policies():
    user_id = 1
    data = request.json
    policy = Policy.query.filter_by(user_id=user_id).first()
    
    if policy:
        if 'autonomous_limit' in data:
            policy.autonomous_limit = data['autonomous_limit']
        if 'daily_limit' in data:
            policy.daily_limit = data['daily_limit']
        if 'monthly_limit' in data:
            policy.monthly_limit = data['monthly_limit']
        if 'new_merchant_approval' in data:
            policy.new_merchant_approval = data['new_merchant_approval']
        if 'high_risk_block' in data:
            policy.high_risk_block = data['high_risk_block']
            
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"error": "Not found"}), 404
