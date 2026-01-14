# **PesaPal Database System**

A complete database system with **MiniDB engine**, **REST API**, and **role-based authentication**.

## **📦 System Components**

1. **MiniDB Engine** - Custom SQL database (port 2500)
2. **REST API** - Flask backend with authentication (port 3500)
3. **Database Seeder** - Populates sample data

## **🚀 Quick Start**

### **1. Start Both Services**
```bash
# Terminal 1: Start MiniDB Database
cd pesapal-rdbms
python server.py

# Terminal 2: Start REST API
cd api
python run.py
```

**Services will run on:**
- MiniDB: http://localhost:2500
- REST API: http://localhost:3500

### **2. Seed Database with Sample Data**
```bash
cd pesapal
python seeder.py
```

This creates:
- 4 default roles (admin, manager, user, viewer)
- 6 sample user accounts
- 10 sample products

## **🔐 Default Test Credentials**

| Role | Username | Password |
|------|----------|----------|
| Admin | `superadmin` | `Admin123!` |
| Manager | `alice_manager` | `Manager123!` |
| User | `bob_sales` | `Sales123!` |
| Viewer | `diana_viewer` | `Viewer123!` |

## **🌐 API Endpoints**

### **Authentication**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/permissions` - Get user permissions

### **Products**
- `GET /api/products` - List all products
- `POST /api/products` - Create product (needs auth)
- `GET /api/products/{id}` - Get single product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### **Users (Admin Only)**
- `GET /api/users` - List all users
- `PUT /api/users/{id}` - Update user
- `POST /api/users/{id}/deactivate` - Deactivate user

### **Roles (Admin Only)**
- `GET /api/auth/roles` - List all roles
- `POST /api/auth/roles` - Create new role

## **🛠️ Testing with cURL**

```bash
# 1. Register a user
curl -X POST http://localhost:3500/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@test.com", "password": "test123", "role": "user"}'

# 2. Login
curl -X POST http://localhost:3500/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test123"}'
# Save the session cookie from response headers

# 3. List products
curl http://localhost:3500/api/products

# 4. Create product (with session cookie)
curl -X POST http://localhost:3500/api/products \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"name": "New Product", "price": 99.99, "stock": 10}'
```

## **📁 Project Structure**
```
pesapal/
├── pesapal-rdbms/     # MiniDB database engine
├── api/               # REST API backend
├── seeder.py          # Database seeder
└── README.md          # This file
```

## **🔄 Reset Database**
```bash
# Stop both services (Ctrl+C)

# Delete data files
cd pesapal-rdbms/data
rm -f *.json *.idx

# Restart services and reseed
cd ../..
python seeder.py
```

## **🔍 Health Checks**
```bash
# Check MiniDB
curl http://localhost:2500/health

# Check REST API
curl http://localhost:3500/health
```

## **⚙️ Configuration**

### **Ports**
- MiniDB: 2500
- REST API: 3500

### **Environment Variables**
Create `.env` file in `api/` folder:
```env
MINIDB_URL=http://localhost:2500
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## **📞 Support**
- **API Documentation**: http://localhost:3500
- **MiniDB Shell**: Use `python main.py` in `pesapal-rdbms/` for SQL shell
- **Postman Collection**: Use the provided endpoints with examples

---

**🚀 Ready to go!** Start both services, run the seeder, and begin testing!