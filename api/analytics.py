# blueprints/analytics.py
from flask import Blueprint, request, jsonify, session
from services.analytics_service import AnalyticsService
from services.auth_service import AuthService

analytics_bp = Blueprint('analytics', __name__)

def require_auth():
    """Decorator to require authentication"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@analytics_bp.route('/dashboard', methods=['GET'])
@require_auth()
def get_dashboard_data():
    """Get dashboard analytics data"""
    try:
        auth_service = AuthService()
        analytics_service = AnalyticsService(auth_service)
        
        user_id = session['user_id']
        dashboard_data = analytics_service.get_dashboard_stats(user_id)
        
        return jsonify(dashboard_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@analytics_bp.route('/overview', methods=['GET'])
@require_auth()
def get_quick_overview():
    """Get quick overview for dashboard cards"""
    try:
        auth_service = AuthService()
        analytics_service = AnalyticsService(auth_service)
        
        user_id = session['user_id']
        dashboard_data = analytics_service.get_dashboard_stats(user_id)
        
        summary = dashboard_data.get('summary', {})
        
        return jsonify({
            'total_products': summary.get('total_products', 0),
            'total_users': summary.get('total_users', 0),
            'total_value': summary.get('total_value', 0),
            'growth_rate': summary.get('growth_rate', 0),
            'low_stock_count': summary.get('low_stock_count', 0),
            'average_price': summary.get('average_price', 0)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@analytics_bp.route('/recent', methods=['GET'])
@require_auth()
def get_recent_activity():
    """Get recent activity for dashboard"""
    try:
        auth_service = AuthService()
        analytics_service = AnalyticsService(auth_service)
        
        user_id = session['user_id']
        dashboard_data = analytics_service.get_dashboard_stats(user_id)
        
        return jsonify({
            'recent_products': dashboard_data.get('recent', {}).get('products', []),
            'recent_users': dashboard_data.get('recent', {}).get('users', []),
            'activity_log': dashboard_data.get('activity', [])
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@analytics_bp.route('/insights', methods=['GET'])
@require_auth()
def get_insights():
    """Get business insights"""
    try:
        auth_service = AuthService()
        analytics_service = AnalyticsService(auth_service)
        
        user_id = session['user_id']
        dashboard_data = analytics_service.get_dashboard_stats(user_id)
        
        return jsonify({
            'insights': dashboard_data.get('insights', {})
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400