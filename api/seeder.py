# seeder.py
import requests
import json
import time
import sys

BASE_URL = "http://localhost:3500"  # Change to your API port

class DatabaseSeeder:
    def __init__(self, base_url=None):
        self.base_url = base_url or BASE_URL
        self.admin_session = None
        
    def wait_for_api(self, max_attempts=30):
        """Wait for API to be ready"""
        print("Waiting for API to be ready...")
        for i in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print("✓ API is ready!")
                    return True
            except requests.exceptions.ConnectionError:
                pass
            
            if i < max_attempts - 1:
                print(f"  Attempt {i+1}/{max_attempts}...")
                time.sleep(1)
        
        print("✗ API not ready after waiting")
        return False
    
    def register_admin(self):
        """Register the first admin user"""
        print("\n" + "="*60)
        print("REGISTERING ADMIN USER")
        print("="*60)
        
        admin_data = {
            "username": "superadmin",
            "email": "admin@company.com",
            "password": "Admin123!",
            "role": "admin"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/register", 
                                   json=admin_data)
            
            if response.status_code == 201:
                print("✓ Admin registered successfully")
                return True
            elif response.status_code == 400:
                data = response.json()
                if "already exists" in data.get('error', ''):
                    print("✓ Admin already exists")
                    return True
                else:
                    print(f"✗ Registration failed: {data}")
                    return False
            else:
                print(f"✗ Unexpected response: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error registering admin: {e}")
            return False
    
    def login_admin(self):
        """Login as admin to get session"""
        print("\n" + "="*60)
        print("LOGGING IN AS ADMIN")
        print("="*60)
        
        login_data = {
            "username": "superadmin",
            "password": "Admin123!"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                                   json=login_data)
            
            if response.status_code == 200:
                print("✓ Admin login successful")
                # Save session cookie
                self.admin_session = response.cookies.get('session')
                return True
            else:
                print(f"✗ Login failed: {response.json()}")
                return False
                
        except Exception as e:
            print(f"✗ Error logging in: {e}")
            return False
    
    def get_session_cookies(self):
        """Get cookies for authenticated requests"""
        if not self.admin_session:
            return {}
        return {'session': self.admin_session}
    
    def create_sample_users(self):
        """Create sample users for all roles"""
        print("\n" + "="*60)
        print("CREATING SAMPLE USERS")
        print("="*60)
        
        sample_users = [
            {
                "username": "alice_manager",
                "email": "alice@store.com",
                "password": "Manager123!",
                "role": "manager",
                "description": "Store Manager"
            },
            {
                "username": "bob_sales",
                "email": "bob@sales.com",
                "password": "Sales123!",
                "role": "user",
                "description": "Sales Representative"
            },
            {
                "username": "charlie_tech",
                "email": "charlie@tech.com",
                "password": "Tech123!",
                "role": "user",
                "description": "Technical Staff"
            },
            {
                "username": "diana_viewer",
                "email": "diana@viewer.com",
                "password": "Viewer123!",
                "role": "viewer",
                "description": "Read-only Viewer"
            },
            {
                "username": "edward_admin",
                "email": "edward@admin.com",
                "password": "Admin456!",
                "role": "admin",
                "description": "Secondary Admin"
            }
        ]
        
        created_count = 0
        for user in sample_users:
            print(f"\nCreating {user['role']}: {user['username']}")
            
            try:
                response = requests.post(f"{self.base_url}/api/auth/register",
                                       json={
                                           "username": user["username"],
                                           "email": user["email"],
                                           "password": user["password"],
                                           "role": user["role"]
                                       })
                
                if response.status_code == 201:
                    print(f"  ✓ Created successfully")
                    created_count += 1
                elif response.status_code == 400:
                    data = response.json()
                    if "already exists" in data.get('error', ''):
                        print(f"  ✓ Already exists")
                        created_count += 1
                    else:
                        print(f"  ✗ Failed: {data.get('error', 'Unknown error')}")
                else:
                    print(f"  ✗ Unexpected: {response.status_code}")
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        print(f"\n✓ Created/verified {created_count} sample users")
        return created_count
    
    def create_sample_products(self):
        """Create sample products for testing"""
        print("\n" + "="*60)
        print("CREATING SAMPLE PRODUCTS")
        print("="*60)
        
        # First login as a manager to create products
        manager_data = {
            "username": "alice_manager",
            "password": "Manager123!"
        }
        
        try:
            # Login as manager
            response = requests.post(f"{self.base_url}/api/auth/login",
                                   json=manager_data)
            
            if response.status_code != 200:
                print("✗ Could not login as manager")
                return 0
                
            manager_session = response.cookies.get('session')
            cookies = {'session': manager_session}
            
        except Exception as e:
            print(f"✗ Error logging in as manager: {e}")
            return 0
        
        sample_products = [
            {
                "name": "MacBook Pro 16",
                "description": "Apple laptop with M3 Max chip, 32GB RAM, 1TB SSD",
                "price": 2499.99,
                "category": "Electronics",
                "stock": 15
            },
            {
                "name": "iPhone 15 Pro",
                "description": "Latest iPhone with titanium design, A17 Pro chip",
                "price": 999.99,
                "category": "Electronics",
                "stock": 45
            },
            {
                "name": "AirPods Pro (2nd Gen)",
                "description": "Wireless earbuds with Active Noise Cancellation",
                "price": 249.99,
                "category": "Audio",
                "stock": 78
            },
            {
                "name": "iPad Air",
                "description": "Thin and lightweight iPad with M1 chip",
                "price": 599.99,
                "category": "Tablets",
                "stock": 32
            },
            {
                "name": "Apple Watch Series 9",
                "description": "Smartwatch with advanced health features",
                "price": 399.99,
                "category": "Wearables",
                "stock": 56
            },
            {
                "name": "Logitech MX Master 3S",
                "description": "Wireless mouse for productivity",
                "price": 99.99,
                "category": "Accessories",
                "stock": 120
            },
            {
                "name": "Samsung 4K Monitor",
                "description": "32-inch 4K UHD monitor for professionals",
                "price": 349.99,
                "category": "Monitors",
                "stock": 22
            },
            {
                "name": "Dell XPS 13",
                "description": "Windows laptop with Intel Core i7, 16GB RAM",
                "price": 1299.99,
                "category": "Electronics",
                "stock": 18
            },
            {
                "name": "Sony WH-1000XM5",
                "description": "Noise cancelling wireless headphones",
                "price": 399.99,
                "category": "Audio",
                "stock": 65
            },
            {
                "name": "Google Pixel 8 Pro",
                "description": "Android smartphone with advanced camera",
                "price": 899.99,
                "category": "Electronics",
                "stock": 28
            }
        ]
        
        created_count = 0
        for i, product in enumerate(sample_products, 1):
            print(f"\nCreating product {i}/{len(sample_products)}: {product['name']}")
            
            try:
                response = requests.post(f"{self.base_url}/api/auth/login",
                                       json=manager_data)
                
                if response.status_code != 200:
                    print(f"  ✗ Login failed")
                    continue
                    
                cookies = {'session': response.cookies.get('session')}
                
                response = requests.post(f"{self.base_url}/api/products",
                                       json=product,
                                       cookies=cookies)
                
                if response.status_code == 201:
                    print(f"  ✓ Created successfully")
                    created_count += 1
                elif response.status_code == 403:
                    print(f"  ✗ Permission denied")
                else:
                    print(f"  ✗ Failed: {response.json()}")
                    
                # Small delay to avoid rate limiting
                time.sleep(0.5)
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        print(f"\n✓ Created {created_count} sample products")
        return created_count
    
    def verify_seeding(self):
        """Verify that seeding was successful"""
        print("\n" + "="*60)
        print("VERIFYING SEEDED DATA")
        print("="*60)
        
        verifications = []
        
        # 1. Check API health
        try:
            response = requests.get(f"{self.base_url}/health")
            verifications.append(("API Health", response.status_code == 200))
        except:
            verifications.append(("API Health", False))
        
        # 2. Check roles exist (need to be logged in)
        if self.admin_session:
            cookies = self.get_session_cookies()
            try:
                response = requests.get(f"{self.base_URL}/api/auth/roles",
                                      cookies=cookies)
                if response.status_code == 200:
                    data = response.json()
                    roles = [role['name'] for role in data.get('roles', [])]
                    has_admin = 'admin' in roles
                    has_manager = 'manager' in roles
                    has_user = 'user' in roles
                    has_viewer = 'viewer' in roles
                    verifications.append(("Roles Created", has_admin and has_manager and has_user and has_viewer))
                else:
                    verifications.append(("Roles Created", False))
            except:
                verifications.append(("Roles Created", False))
        
        # 3. Try to get products (public endpoint)
        try:
            response = requests.get(f"{self.base_url}/api/products")
            if response.status_code == 200:
                data = response.json()
                product_count = len(data.get('products', []))
                verifications.append((f"Products Available ({product_count})", product_count > 0))
            else:
                verifications.append(("Products Available", False))
        except:
            verifications.append(("Products Available", False))
        
        # Print verification results
        print("\nVerification Results:")
        print("-" * 40)
        for check, status in verifications:
            status_symbol = "✓" if status else "✗"
            print(f"{status_symbol} {check}")
        
        # Summary
        success_count = sum(1 for _, status in verifications if status)
        total_count = len(verifications)
        
        print(f"\n{'='*60}")
        print(f"SEEDING SUMMARY: {success_count}/{total_count} checks passed")
        print(f"{'='*60}")
        
        if success_count == total_count:
            print("✅ Database seeding completed successfully!")
        else:
            print("⚠️  Database seeding completed with some issues")
        
        return success_count == total_count
    
    def print_credentials(self):
        """Print all created credentials for testing"""
        print("\n" + "="*60)
        print("TEST CREDENTIALS")
        print("="*60)
        
        credentials = [
            {"Role": "Admin", "Username": "superadmin", "Password": "Admin123!", "Email": "admin@company.com"},
            {"Role": "Admin 2", "Username": "edward_admin", "Password": "Admin456!", "Email": "edward@admin.com"},
            {"Role": "Manager", "Username": "alice_manager", "Password": "Manager123!", "Email": "alice@store.com"},
            {"Role": "User", "Username": "bob_sales", "Password": "Sales123!", "Email": "bob@sales.com"},
            {"Role": "User", "Username": "charlie_tech", "Password": "Tech123!", "Email": "charlie@tech.com"},
            {"Role": "Viewer", "Username": "diana_viewer", "Password": "Viewer123!", "Email": "diana@viewer.com"}
        ]
        
        print("\nUser Accounts:")
        print("-" * 80)
        print(f"{'Role':<12} {'Username':<20} {'Password':<15} {'Email':<30}")
        print("-" * 80)
        
        for cred in credentials:
            print(f"{cred['Role']:<12} {cred['Username']:<20} {cred['Password']:<15} {cred['Email']:<30}")
        
        print("\n" + "="*60)
        print("TEST ENDPOINTS")
        print("="*60)
        
        endpoints = [
            {"Method": "POST", "Endpoint": "/api/auth/register", "Description": "Register new user"},
            {"Method": "POST", "Endpoint": "/api/auth/login", "Description": "Login user"},
            {"Method": "GET", "Endpoint": "/api/products", "Description": "List all products"},
            {"Method": "POST", "Endpoint": "/api/products", "Description": "Create product (needs auth)"},
            {"Method": "GET", "Endpoint": "/api/auth/permissions", "Description": "Get user permissions"},
            {"Method": "GET", "Endpoint": "/api/users", "Description": "List users (admin only)"},
            {"Method": "GET", "Endpoint": "/api/auth/roles", "Description": "List roles (admin only)"}
        ]
        
        print("\nKey API Endpoints:")
        print("-" * 80)
        print(f"{'Method':<8} {'Endpoint':<30} {'Description':<40}")
        print("-" * 80)
        
        for endpoint in endpoints:
            print(f"{endpoint['Method']:<8} {endpoint['Endpoint']:<30} {endpoint['Description']:<40}")
    
    def run(self):
        """Run the complete seeding process"""
        print("\n" + "="*60)
        print("DATABASE SEEDER")
        print("="*60)
        print("This script will populate your database with sample data.")
        print("Make sure your MiniDB and REST API are running!")
        print("="*60)
        
        # Wait for API
        if not self.wait_for_api():
            print("\n❌ Please start your REST API and MiniDB first!")
            print("1. Start MiniDB: cd pesapal-rdbms && python server.py")
            print("2. Start API: cd api && python run.py")
            sys.exit(1)
        
        # Register admin
        if not self.register_admin():
            print("\n❌ Failed to register admin user")
            sys.exit(1)
        
        # Login admin
        if not self.login_admin():
            print("\n❌ Failed to login as admin")
            sys.exit(1)
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample products
        self.create_sample_products()
        
        # Verify everything
        self.verify_seeding()
        
        # Print credentials
        self.print_credentials()
        
        print("\n" + "="*60)
        print("✅ SEEDING COMPLETE!")
        print("="*60)
        print("\nYour database is now populated with:")
        print("  • 4 default roles (admin, manager, user, viewer)")
        print("  • 16 default permissions")
        print("  • 6 sample user accounts")
        print("  • 10 sample products")
        print("\nUse the credentials above to test different roles.")
        print("="*60)

if __name__ == "__main__":
    # You can specify a different port if needed
    # seeder = DatabaseSeeder("http://localhost:5000")
    seeder = DatabaseSeeder()
    seeder.run()