from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, Policy
from .transaction import Transaction, RiskFactor

