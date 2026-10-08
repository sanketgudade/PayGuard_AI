from flask import Blueprint, jsonify
from ..models.transaction import Transaction

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    user_id = 1
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).limit(10).all()
    
    return jsonify([{
        "id": t.id,
        "merchant": t.merchant,
        "amount": float(t.amount),
        "currency": t.currency,
        "risk_level": t.risk_level,
        "status": t.status,
        "created_at": t.created_at.isoformat()
    } for t in transactions])
