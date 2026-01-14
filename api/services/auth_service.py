import hashlib
import time
import json
from services.database import MiniDBClient

class AuthService:
    """Authentication and user management service with role-based permissions"""
    
    def __init__(self):
        self.db = MiniDBClient()
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize default roles and permissions"""
        # Check if roles table is empty
        roles = self.db.select('roles')
        if not roles:
            self._create_default_roles_and_permissions()
    
    def _create_default_roles_and_permissions(self):
        """Create default roles and permissions"""
        from config import Config
        
        # Create permissions
        permission_map = {}
        for perm_name, perm_desc in Config.DEFAULT_PERMISSIONS:
            perm_id = int(time.time() * 1000) + len(permission_map)
            self.db.insert('permissions', {
                'id': perm_id,
                'name': perm_name,
                'description': perm_desc
            })
            permission_map[perm_name] = perm_id
        
        # Create roles with permissions
        for role_name, permissions in Config.DEFAULT_ROLES.items():
            role_id = int(time.time() * 1000) + hash(role_name) % 1000
            
            # Create role
            self.db.insert('roles', {
                'id': role_id,
                'name': role_name,
                'permissions': json.dumps(permissions)  # Store as JSON for quick access
            })
            
            # Link role to permissions
            for perm_name in permissions:
                if perm_name in permission_map:
                    self.db.insert('role_permissions', {
                        'role_id': role_id,
                        'permission_id': permission_map[perm_name]
                    })
        
        print("Default roles and permissions created")
    
    def hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password, role_name='user'):
        """Register a new user with role"""
        # Check if user exists
        existing = self.db.select('users', f"username = '{username}' OR email = '{email}'")
        if existing:
            raise Exception("Username or email already exists")
        
        # Get role_id
        roles = self.db.select('roles', f"name = '{role_name}'")
        if not roles:
            raise Exception(f"Role '{role_name}' does not exist")
        
        role_id = roles[0][0]  # First column is id
        
        # Create user
        user_id = int(time.time() * 1000)
        password_hash = self.hash_password(password)
        
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role_id': role_id,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': 1
        }
        
        self.db.insert('users', user_data)
        return user_id
    
    def authenticate_user(self, username, password):
        """Authenticate user and return user data with role info"""
        users = self.db.select('users', f"username = '{username}' AND is_active = 1")
        
        if not users:
            return None
        
        user_row = users[0]
        password_hash = self.hash_password(password)
        
        # Assuming columns: id, username, email, password_hash, role_id, created_at, is_active
        if user_row[3] == password_hash:  # password_hash at index 3
            # Get role information
            role = self.get_role_by_id(user_row[4])
            
            return {
                'id': user_row[0],
                'username': user_row[1],
                'email': user_row[2],
                'role_id': user_row[4],
                'role_name': role['name'] if role else 'user',
                'permissions': role['permissions'] if role else [],
                'created_at': user_row[5]
            }
        
        return None
    
    def get_role_by_id(self, role_id):
        """Get role by ID"""
        roles = self.db.select('roles', f"id = {role_id}")
        if not roles:
            return None
        
        role_row = roles[0]
        return {
            'id': role_row[0],
            'name': role_row[1],
            'permissions': json.loads(role_row[2]) if role_row[2] else []
        }
    
    def get_role_by_name(self, role_name):
        """Get role by name"""
        roles = self.db.select('roles', f"name = '{role_name}'")
        if not roles:
            return None
        
        role_row = roles[0]
        return {
            'id': role_row[0],
            'name': role_row[1],
            'permissions': json.loads(role_row[2]) if role_row[2] else []
        }
    
    def get_user_by_id(self, user_id):
        """Get user by ID with role info"""
        users = self.db.select('users', f"id = {user_id}")
        if not users:
            return None
        
        user_row = users[0]
        
        # Get role information
        role = self.get_role_by_id(user_row[4])
        
        return {
            'id': user_row[0],
            'username': user_row[1],
            'email': user_row[2],
            'role_id': user_row[4],
            'role_name': role['name'] if role else 'user',
            'permissions': role['permissions'] if role else [],
            'created_at': user_row[5],
            'is_active': bool(user_row[6])
        }
    
    def update_user_role(self, user_id, new_role_name):
        """Update user's role"""
        # Get new role
        new_role = self.get_role_by_name(new_role_name)
        if not new_role:
            raise Exception(f"Role '{new_role_name}' does not exist")
        
        # Update user
        return self.db.update('users', {'role_id': new_role['id']}, f"id = {user_id}")
    
    def has_permission(self, user_id, permission_name):
        """Check if user has specific permission"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        return permission_name in user['permissions']
    
    def get_all_roles(self):
        """Get all roles"""
        roles_data = self.db.select('roles', columns='*')
        roles = []
        
        for row in roles_data:
            roles.append({
                'id': row[0],
                'name': row[1],
                'permissions': json.loads(row[2]) if row[2] else []
            })
        
        return roles
    
    def create_role(self, name, permissions):
        """Create a new role"""
        # Check if role exists
        existing = self.db.select('roles', f"name = '{name}'")
        if existing:
            raise Exception(f"Role '{name}' already exists")
        
        # Create role
        role_id = int(time.time() * 1000)
        self.db.insert('roles', {
            'id': role_id,
            'name': name,
            'permissions': json.dumps(permissions)
        })
        
        return role_id
    
    def update_role_permissions(self, role_name, permissions):
        """Update role permissions"""
        role = self.get_role_by_name(role_name)
        if not role:
            raise Exception(f"Role '{role_name}' does not exist")
        
        return self.db.update('roles', 
                            {'permissions': json.dumps(permissions)}, 
                            f"id = {role['id']}")
    
    def update_user(self, user_id, updates):
        """Update user information"""
        where = f"id = {user_id}"
        
        # Don't allow password update through this method
        if 'password_hash' in updates:
            del updates['password_hash']
        
        # If updating role, convert role_name to role_id
        if 'role' in updates:
            role_name = updates.pop('role')
            role = self.get_role_by_name(role_name)
            if not role:
                raise Exception(f"Role '{role_name}' does not exist")
            updates['role_id'] = role['id']
        
        return self.db.update('users', updates, where)
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")
        
        # Verify old password
        auth_user = self.authenticate_user(user['username'], old_password)
        if not auth_user:
            raise Exception("Current password is incorrect")
        
        # Update password
        new_hash = self.hash_password(new_password)
        return self.db.update('users', {'password_hash': new_hash}, f"id = {user_id}")