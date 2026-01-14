from flask import Blueprint, request, jsonify, session
from services.auth_service import AuthService
from services.permission_service import PermissionService

users_bp = Blueprint('users', __name__)
auth_service = AuthService()
permission_service = PermissionService(auth_service)

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

def require_admin():
    """Decorator to require admin role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            if not permission_service.check_permission(session['user_id'], 'manage_roles'):
                return jsonify({'error': 'Admin access required'}), 403
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@users_bp.route('', methods=['GET'])
@require_auth()
def get_users():
    """Get all users (requires user management permission)"""
    if not permission_service.can_manage_users(session['user_id']):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        from services.database import MiniDBClient
        db = MiniDBClient()
        users_data = db.select('users')
        
        users = []
        for row in users_data:
            # Get role info
            role = auth_service.get_role_by_id(row[4])
            
            users.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'role_id': row[4],
                'role_name': role['name'] if role else 'Unknown',
                'created_at': row[5],
                'is_active': bool(row[6])
            })
        
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/<int:user_id>', methods=['GET'])
@require_auth()
def get_user(user_id):
    """Get user by ID (admin only)"""
    # Check if user has permission to view users
    if not (permission_service.check_permission(session['user_id'], 'view_users') or
            permission_service.check_permission(session['user_id'], 'manage_roles')):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        user = auth_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/<int:user_id>', methods=['PUT'])
@require_auth()
def update_user(user_id):
    """Update user (admin only)"""
    # Check if user has permission to update users
    if not (permission_service.check_permission(session['user_id'], 'update_user') or
            permission_service.check_permission(session['user_id'], 'manage_roles')):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.json
        
        # Don't allow password updates through this endpoint
        if 'password' in data:
            del data['password']
        
        auth_service.update_user(user_id, data)
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/<int:user_id>/role', methods=['PUT'])
@require_auth()
def update_user_role(user_id):
    """Update user role (admin only)"""
    # Check if user has permission to manage roles
    if not permission_service.check_permission(session['user_id'], 'manage_roles'):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.json
        
        if 'role' not in data:
            return jsonify({'error': 'Missing role field'}), 400
        
        auth_service.update_user_role(user_id, data['role'])
        
        return jsonify({'message': 'User role updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/<int:user_id>/deactivate', methods=['POST'])
@require_auth()
def deactivate_user(user_id):
    """Deactivate user (admin only)"""
    # Check if user has permission to manage users
    if not (permission_service.check_permission(session['user_id'], 'delete_user') or
            permission_service.check_permission(session['user_id'], 'manage_roles')):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        from services.database import MiniDBClient
        db = MiniDBClient()
        db.update('users', {'is_active': 0}, f"id = {user_id}")
        return jsonify({'message': 'User deactivated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@users_bp.route('/<int:user_id>/activate', methods=['POST'])
@require_auth()
def activate_user(user_id):
    """Activate user (admin only)"""
    # Check if user has permission to manage users
    if not (permission_service.check_permission(session['user_id'], 'update_user') or
            permission_service.check_permission(session['user_id'], 'manage_roles')):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        from services.database import MiniDBClient
        db = MiniDBClient()
        db.update('users', {'is_active': 1}, f"id = {user_id}")
        return jsonify({'message': 'User activated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400