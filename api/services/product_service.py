import time
from services.database import MiniDBClient

class ProductService:
    """Product management service"""
    
    def __init__(self):
        self.db = MiniDBClient()
    
    def create_product(self, product_data, created_by):
        """Create a new product"""
        product_id = int(time.time() * 1000)
        
        product = {
            'id': product_id,
            'name': product_data['name'],
            'description': product_data.get('description', ''),
            'price': str(product_data['price']),  # Convert to string
            'category': product_data.get('category', ''),
            'stock': int(product_data.get('stock', 0)),
            'created_by': created_by,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"DEBUG: Creating product with data: {product}")
        
        try:
            self.db.insert('products', product)
            print(f"DEBUG: Product inserted with ID: {product_id}")
        except Exception as e:
            print(f"DEBUG: Error inserting product: {e}")
            raise
        
        return product_id
    
    def get_all_products(self, page=1, per_page=20):
        """Get all products with pagination (basic)"""
        products = self.db.select('products', columns='*')
        
        # Simple pagination (MiniDB doesn't have LIMIT/OFFSET yet)
        start = (page - 1) * per_page
        end = start + per_page
        paginated = products[start:end]
        
        # Convert to dictionaries
        result = []
        for row in paginated:
            result.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'category': row[4],
                'stock': row[5],
                'created_by': row[6],
                'created_at': row[7],
                'updated_at': row[8]
            })
        
        return {
            'products': result,
            'total': len(products),
            'page': page,
            'per_page': per_page,
            'total_pages': (len(products) + per_page - 1) // per_page
        }
    
    def get_product(self, product_id):
        """Get single product by ID"""
        products = self.db.select('products', f"id = {product_id}")
        if not products:
            return None
        
        row = products[0]
        return {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': row[3],
            'category': row[4],
            'stock': row[5],
            'created_by': row[6],
            'created_at': row[7],
            'updated_at': row[8]
        }
    
    def update_product(self, product_id, updates, updated_by=None):
        """Update product"""
        # Add updated timestamp
        updates['updated_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        where = f"id = {product_id}"
        return self.db.update('products', updates, where)
    
    def delete_product(self, product_id):
        """Delete product"""
        where = f"id = {product_id}"
        return self.db.delete('products', where)
    
    def search_products(self, query, category=None):
        """Search products by name or description"""
        # Simple search (MiniDB doesn't have LIKE yet)
        all_products = self.db.select('products')
        
        results = []
        for row in all_products:
            name = str(row[1] or '').lower()
            description = str(row[2] or '').lower()
            cat = str(row[4] or '').lower()
            
            query_lower = query.lower()
            
            if query_lower in name or query_lower in description:
                if category and cat != category.lower():
                    continue
                
                results.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'category': row[4],
                    'stock': row[5],
                    'created_by': row[6]
                })
        
        return results