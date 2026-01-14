from flask import Blueprint, request, jsonify, session
from services.product_service import ProductService
from services.auth_service import AuthService
from services.permission_service import PermissionService
from utils.validators import Validators

products_bp = Blueprint('products', __name__)
product_service = ProductService()
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

def require_permission(permission_name):
    """Decorator to require specific permission"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            if not permission_service.check_permission(session['user_id'], permission_name):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

@products_bp.route('', methods=['GET'])
def get_products():
    """Get all products (with permission check)"""
    try:
        # Check if user can view products
        if not permission_service.can_view_product(session.get('user_id')):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        result = product_service.get_all_products(page, per_page)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    try:
        # Check if user can view products
        if not permission_service.can_view_product(session.get('user_id')):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        product = product_service.get_product(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'product': product}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('', methods=['POST'])
@require_auth()
def create_product():
    """Create new product - check create permission"""
    try:
        data = request.json
        
        # Check permission
        if not (permission_service.check_permission(session['user_id'], 'create_product') or
                permission_service.check_permission(session['user_id'], 'create_own_product')):
            return jsonify({'error': 'Insufficient permissions to create product'}), 403
        
        # Validate product data
        is_valid, errors = Validators.validate_product_data(data)
        if not is_valid:
            return jsonify({'error': errors}), 400
        
        # Create product
        product_id = product_service.create_product(
            product_data=data,
            created_by=session['user_id']
        )
        
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['PUT'])
@require_auth()
def update_product(product_id):
    """Update product with permission check"""
    try:
        data = request.json
        
        # Check if product exists
        existing = product_service.get_product(product_id)
        if not existing:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check permission
        if not permission_service.can_edit_product(session['user_id'], existing['created_by']):
            return jsonify({'error': 'Not authorized to update this product'}), 403
        
        # Validate updates
        if 'price' in data or 'stock' in data:
            is_valid, errors = Validators.validate_product_data(data)
            if not is_valid:
                return jsonify({'error': errors}), 400
        
        # Update product
        product_service.update_product(product_id, data, session['user_id'])
        
        return jsonify({'message': 'Product updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@require_auth()
def delete_product(product_id):
    """Delete product with permission check"""
    try:
        # Check if product exists
        existing = product_service.get_product(product_id)
        if not existing:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check permission
        if not permission_service.can_delete_product(session['user_id'], existing['created_by']):
            return jsonify({'error': 'Not authorized to delete this product'}), 403
        
        # Delete product
        product_service.delete_product(product_id)
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@products_bp.route('/search', methods=['GET'])
def search_products():
    """Search products"""
    try:
        # Check if user can view products
        if not permission_service.can_view_product(session.get('user_id')):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        query = request.args.get('q', '')
        category = request.args.get('category')
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        results = product_service.search_products(query, category)
        return jsonify({'results': results, 'count': len(results)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400