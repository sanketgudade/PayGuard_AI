from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Policy(db.Model):
    __tablename__ = 'policies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    autonomous_limit = db.Column(db.Numeric(10, 2), default=100.00)
    daily_limit = db.Column(db.Numeric(10, 2), default=500.00)
    monthly_limit = db.Column(db.Numeric(10, 2), default=2000.00)
    new_merchant_approval = db.Column(db.Boolean, default=True)
    high_risk_block = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
