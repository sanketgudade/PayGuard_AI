from flask import Blueprint, request, jsonify
from ..services.paypal_service import create_order, capture_order

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/create-order', methods=['POST'])
def create_paypal_order():
    data = request.json
    amount = data.get('amount')
    currency = data.get('currency', 'USD')
    
    order = create_order(amount, currency)
    return jsonify(order)

@payments_bp.route('/capture-order', methods=['POST'])
def capture_paypal_order():
    data = request.json
    order_id = data.get('order_id')
    
    capture = capture_order(order_id)
    return jsonify(capture)
