from . import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    merchant = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    risk_score = db.Column(db.Integer)
    risk_level = db.Column(db.String(20))
    decision = db.Column(db.String(50))
    paypal_order_id = db.Column(db.String(100))
    paypal_capture_id = db.Column(db.String(100))
    status = db.Column(db.String(50), default='ANALYZING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RiskFactor(db.Model):
    __tablename__ = 'risk_factors'
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    factor_type = db.Column(db.String(50))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
