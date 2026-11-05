from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import db

def init_database(app):
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///payguard.db')
    if 'mysql' in db_uri:
        from sqlalchemy import create_engine
        try:
            test_engine = create_engine(db_uri, connect_args={'connect_timeout': 2})
            with test_engine.connect() as conn:
                pass
            test_engine.dispose()
        except Exception:
            # Fallback to SQLite if MySQL is unreachable or not running
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payguard.db'
            
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
            from .models.user import User, Policy
            from .models.transaction import Transaction
            if not User.query.first():
                demo_user = User(name='Sanket Gudade', email='sanket@payguard.ai')
                db.session.add(demo_user)
                db.session.commit()
                demo_policy = Policy(
                    user_id=demo_user.id,
                    autonomous_limit=500.0,
                    daily_limit=1500.0,
                    monthly_limit=10000.0,
                    new_merchant_approval=True,
                    high_risk_block=True
                )
                db.session.add(demo_policy)
                
                # Seed initial demo transactions
                sample_txs = [
                    Transaction(user_id=demo_user.id, merchant='TechStore', amount=45.00, currency='USD', category='Electronics', description='AI Hardware accessory', risk_score=12, risk_level='LOW', decision='APPROVED', paypal_order_id='PAYPAL_ORDER_8F9A1B2C', paypal_capture_id='PAYPAL_CAPTURE_7E6D5C4B', status='COMPLETED'),
                    Transaction(user_id=demo_user.id, merchant='UnknownShop', amount=850.00, currency='USD', category='Digital Goods', description='High-value digital asset purchase', risk_score=72, risk_level='HIGH', decision='BLOCKED', status='BLOCKED'),
                    Transaction(user_id=demo_user.id, merchant='MacBook Pro Reseller', amount=1249.00, currency='USD', category='Electronics', description='Hardware procurement', risk_score=34, risk_level='MEDIUM', decision='REVIEW', status='PENDING_APPROVAL'),
                    Transaction(user_id=demo_user.id, merchant='CoffeeHouse', amount=4.50, currency='USD', category='Food & Beverage', description='Morning espresso subscription', risk_score=5, risk_level='LOW', decision='APPROVED', paypal_order_id='PAYPAL_ORDER_1A2B3C4D', paypal_capture_id='PAYPAL_CAPTURE_9Z8Y7X6W', status='COMPLETED')
                ]
                db.session.add_all(sample_txs)
                db.session.commit()
        except Exception:
            pass

def create_app():
    # Tell Flask to use the 'PayGuard_UI' folder for templates and static files
    import os
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'PayGuard_UI'))
    
    app = Flask(__name__, template_folder=frontend_dir, static_folder=frontend_dir, static_url_path='/static')
    app.config.from_object(Config)
    CORS(app)
    
    init_database(app)
    
    from .routes.ai import ai_bp
    from .routes.payments import payments_bp
    from .routes.policies import policies_bp
    from .routes.transactions import transactions_bp
    
    app.register_blueprint(ai_bp, url_prefix='/api/agent')
    app.register_blueprint(payments_bp, url_prefix='/api/paypal')
    app.register_blueprint(policies_bp, url_prefix='/api/policies')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    
    @app.route('/health')
    def health():
        return {"status": "ok"}
        
    # Frontend Routes
    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard.html')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/agent.html')
    def agent():
        return render_template('agent.html')

    @app.route('/settings.html')
    def settings():
        return render_template('settings.html')

    @app.route('/transactions.html')
    def transactions():
        return render_template('transactions.html')
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
