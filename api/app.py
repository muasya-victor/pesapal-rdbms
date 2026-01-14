from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from services.database import MiniDBClient

# Import blueprints
from auth import auth_bp
from products import products_bp
from users import users_bp
from analytics import analytics_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend development
    CORS(app, supports_credentials=True)
    
    # Set secret key for sessions
    app.secret_key = Config.SECRET_KEY
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix=Config.API_PREFIX + '/auth')
    app.register_blueprint(products_bp, url_prefix=Config.API_PREFIX + '/products')
    app.register_blueprint(users_bp, url_prefix=Config.API_PREFIX + '/users')
    app.register_blueprint(analytics_bp, url_prefix=Config.API_PREFIX + '/analytics')
    
    # Initialize database - using modern Flask approach
    with app.app_context():
        try:
            db_client = MiniDBClient()
            db_client.initialize_database()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'MiniDB API',
            'database': 'MiniDB'
        }), 200
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'MiniDB REST API',
            'version': '1.0',
            'endpoints': {
                'auth': Config.API_PREFIX + '/auth',
                'products': Config.API_PREFIX + '/products',
                'users': Config.API_PREFIX + '/users'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)