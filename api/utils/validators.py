import re

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        return True, ""
    
    @staticmethod
    def validate_product_data(data):
        """Validate product data"""
        errors = []
        
        if 'name' not in data or not data['name'].strip():
            errors.append("Product name is required")
        
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    errors.append("Price must be positive")
            except ValueError:
                errors.append("Price must be a valid number")
        
        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    errors.append("Stock cannot be negative")
            except ValueError:
                errors.append("Stock must be a valid integer")
        
        return len(errors) == 0, errors