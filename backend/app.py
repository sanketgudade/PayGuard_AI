from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import db

def create_app():
    # Tell Flask to use the 'PayGuard_UI' folder for templates and static files
    import os
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'PayGuard_UI'))
    
    app = Flask(__name__, template_folder=frontend_dir, static_folder=frontend_dir, static_url_path='/static')
    app.config.from_object(Config)
    CORS(app)
    
    db.init_app(app)
    
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
