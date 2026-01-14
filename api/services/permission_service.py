from services.database import MiniDBClient
import json

class PermissionService:
    """Service for checking user permissions"""
    
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def check_permission(self, user_id, permission_name):
        """Check if user has permission"""
        return self.auth_service.has_permission(user_id, permission_name)
    
    def get_user_permissions(self, user_id):
        """Get all permissions for a user"""
        user = self.auth_service.get_user_by_id(user_id)
        return user.get('permissions', []) if user else []
    
    def can_view_product(self, user_id, product_creator_id=None):
        """Check if user can view product"""
        if self.auth_service.has_permission(user_id, 'view_all_products'):
            return True
        
        if self.auth_service.has_permission(user_id, 'view_products'):
            return True
        
        return False
    
    def can_edit_product(self, user_id, product_creator_id):
        """Check if user can edit product"""
        # Admins and managers can edit any product
        if (self.auth_service.has_permission(user_id, 'update_product') or 
            self.auth_service.has_permission(user_id, 'manage_roles')):
            return True
        
        # Users can edit their own products
        if (self.auth_service.has_permission(user_id, 'update_own_product') and 
            user_id == product_creator_id):
            return True
        
        return False
    
    def can_delete_product(self, user_id, product_creator_id):
        """Check if user can delete product"""
        # Admins and managers can delete any product
        if (self.auth_service.has_permission(user_id, 'delete_product') or 
            self.auth_service.has_permission(user_id, 'manage_roles')):
            return True
        
        # Users can delete their own products
        if (self.auth_service.has_permission(user_id, 'delete_own_product') and 
            user_id == product_creator_id):
            return True
        
        return False
    
    def can_manage_users(self, user_id):
        """Check if user can manage users"""
        return (self.auth_service.has_permission(user_id, 'create_user') or
                self.auth_service.has_permission(user_id, 'update_user') or
                self.auth_service.has_permission(user_id, 'delete_user') or
                self.auth_service.has_permission(user_id, 'manage_roles'))