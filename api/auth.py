from flask import Blueprint, request, jsonify, session
from services.auth_service import AuthService
from services.permission_service import PermissionService
from utils.validators import Validators

auth_bp = Blueprint('auth', __name__)
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

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        
        # Validate input
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not Validators.validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        is_valid, msg = Validators.validate_password(data['password'])
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Get role from request or default to 'user'
        role_name = data.get('role', 'user')
        
        # Register user
        user_id = auth_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role_name=role_name  # Changed from role to role_name
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'role': role_name
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        
        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Username and password required'}), 400
        
        user = auth_service.authenticate_user(data['username'], data['password'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Store user in session
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role_name'] = user['role_name']
        session['permissions'] = user['permissions']
        
        return jsonify({
            'message': 'Login successful',
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile', methods=['GET'])
@require_auth()
def get_profile():
    """Get current user profile"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = auth_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user}), 200

@auth_bp.route('/change-password', methods=['POST'])
@require_auth()
def change_password():
    """Change password"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    if not all(k in data for k in ['old_password', 'new_password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    is_valid, msg = Validators.validate_password(data['new_password'])
    if not is_valid:
        return jsonify({'error': msg}), 400
    
    try:
        auth_service.change_password(user_id, data['old_password'], data['new_password'])
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/roles', methods=['GET'])
@require_auth()
def get_roles():
    """Get all roles (admin only)"""
    # Check if user has permission to manage roles
    if not permission_service.check_permission(session['user_id'], 'manage_roles'):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        roles = auth_service.get_all_roles()
        return jsonify({'roles': roles}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/roles', methods=['POST'])
@require_auth()
def create_role():
    """Create a new role (admin only)"""
    # Check if user has permission to manage roles
    if not permission_service.check_permission(session['user_id'], 'manage_roles'):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.json
        
        if not all(k in data for k in ['name', 'permissions']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        role_id = auth_service.create_role(data['name'], data['permissions'])
        
        return jsonify({
            'message': 'Role created successfully',
            'role_id': role_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/roles/<role_name>', methods=['PUT'])
@require_auth()
def update_role(role_name):
    """Update role permissions (admin only)"""
    # Check if user has permission to manage roles
    if not permission_service.check_permission(session['user_id'], 'manage_roles'):
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = request.json
        
        if 'permissions' not in data:
            return jsonify({'error': 'Missing permissions field'}), 400
        
        auth_service.update_role_permissions(role_name, data['permissions'])
        
        return jsonify({'message': 'Role updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/permissions', methods=['GET'])
@require_auth()
def get_user_permissions():
    """Get current user's permissions"""
    try:
        permissions = permission_service.get_user_permissions(session['user_id'])
        return jsonify({'permissions': permissions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/check-permission', methods=['POST'])
@require_auth()
def check_permission():
    """Check if user has specific permission"""
    try:
        data = request.json
        
        if 'permission' not in data:
            return jsonify({'error': 'Missing permission field'}), 400
        
        has_perm = permission_service.check_permission(
            session['user_id'], 
            data['permission']
        )
        
        return jsonify({
            'has_permission': has_perm,
            'permission': data['permission']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400