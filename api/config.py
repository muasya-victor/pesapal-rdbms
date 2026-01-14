import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MiniDB configuration
    MINIDB_URL = os.getenv('MINIDB_URL', 'http://localhost:2500')
    
    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # API configuration
    API_PREFIX = '/api'
    
    # Database tables (will be created on first run)
    TABLES = {
        'users': """
            CREATE TABLE users (
                id INT PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT,
                role_id INT,
                created_at TEXT,
                is_active INT DEFAULT 1
            )
        """,
        'roles': """
            CREATE TABLE roles (
                id INT PRIMARY KEY,
                name TEXT UNIQUE,
                permissions TEXT  -- JSON string of permissions
            )
        """,
        'permissions': """
            CREATE TABLE permissions (
                id INT PRIMARY KEY,
                name TEXT UNIQUE,
                description TEXT
            )
        """,
        'role_permissions': """
            CREATE TABLE role_permissions (
                role_id INT,
                permission_id INT,
                PRIMARY KEY (role_id, permission_id)
            )
        """,
        'products': """
            CREATE TABLE products (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                category TEXT,
                stock INT DEFAULT 0,
                created_by INT,
                created_at TEXT,
                updated_at TEXT
            )
        """
    }
    
    # Default roles and permissions
    DEFAULT_ROLES = {
        'admin': ['create_user', 'update_user', 'delete_user', 'view_all_products', 
                  'create_product', 'update_product', 'delete_product', 'manage_roles',
                  'view_users', 'update_stock', 'view_profile', 'update_profile'],
        'manager': ['view_all_products', 'create_product', 'update_product', 
                    'view_users', 'update_stock', 'view_profile', 'update_profile'],
        'user': ['view_products', 'create_own_product', 'update_own_product', 
                 'delete_own_product', 'view_profile', 'update_profile'],
        'viewer': ['view_products', 'view_profile']
    }
    
    DEFAULT_PERMISSIONS = [
        ('create_user', 'Create new users'),
        ('update_user', 'Update user information'),
        ('delete_user', 'Delete users'),
        ('view_users', 'View all users'),
        ('create_product', 'Create new products'),
        ('update_product', 'Update any product'),
        ('delete_product', 'Delete any product'),
        ('view_all_products', 'View all products'),
        ('view_products', 'View products'),
        ('create_own_product', 'Create own products'),
        ('update_own_product', 'Update own products'),
        ('delete_own_product', 'Delete own products'),
        ('update_stock', 'Update product stock'),
        ('manage_roles', 'Manage roles and permissions'),
        ('view_profile', 'View own profile'),
        ('update_profile', 'Update own profile')
    ]