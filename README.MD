# **PesaPal Database System**

A complete **end-to-end database platform** featuring a **custom MiniDB engine**, **REST API**, **database seeder**, and a **Next.js UI**, all working together with **role-based authentication**.

--- 

* Youtube WalkThrough: [https://www.youtube.com/watch?v=I64AVCBLfWw](https://www.youtube.com/watch?v=I64AVCBLfWw)

---

## **📦 System Components**

1. **MiniDB Engine**
   Custom SQL-like database engine
   Port: **2500**

2. **REST API**
   Flask backend with authentication & RBAC
   Port: **3500**

3. **Database Seeder**
   Populates MiniDB with initial data

4. **UI Demo (Next.js)**
   Frontend consuming the REST API
   Port: **3000**

---

## **🚀 Quick Start**

### **1. Start All Services**

```bash
# Setup Environment
python -m venv .venv

# Activate Environment
source .venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Terminal 1: Start MiniDB Database
cd pesapal-rdbms
python server.py

# Terminal 2: Start REST API
cd api
python run.py

# Terminal 3: Start UI
cd rdbms-ui-demo
npm install
npm run dev
```

**Services will run on:**

* MiniDB → [http://localhost:2500](http://localhost:2500)
* REST API → [http://localhost:3500](http://localhost:3500)
* UI → [http://localhost:3000](http://localhost:3000)

---

### **2. Seed Database with Sample Data**

```bash
cd pesapal
python seeder.py
```

This creates:

* **4 default roles** (admin, manager, user, viewer)
* **6 sample users**
* **10 sample products**

---

## **🔐 Default Test Credentials**

| Role    | Username        | Password      |
| ------- | --------------- | ------------- |
| Admin   | `superadmin`    | `Admin123!`   |
| Manager | `alice_manager` | `Manager123!` |
| User    | `bob_sales`     | `Sales123!`   |
| Viewer  | `diana_viewer`  | `Viewer123!`  |

These credentials work for:

* **API (cURL / Postman)**
* **Next.js UI**

---

## **🌐 REST API Endpoints**

### **Authentication**

* `POST /api/auth/register`
* `POST /api/auth/login`
* `GET /api/auth/profile`
* `GET /api/auth/permissions`

### **Products**

* `GET /api/products`
* `POST /api/products`
* `GET /api/products/{id}`
* `PUT /api/products/{id}`
* `DELETE /api/products/{id}`

### **Users (Admin Only)**

* `GET /api/users`
* `PUT /api/users/{id}`
* `POST /api/users/{id}/deactivate`

### **Roles (Admin Only)**

* `GET /api/auth/roles`
* `POST /api/auth/roles`

---

## **🛠️ Testing with cURL**

```bash
# Register
curl -X POST http://localhost:3500/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"test123","role":"user"}'

# Login
curl -X POST http://localhost:3500/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'

# List products
curl http://localhost:3500/api/products

# Create product
curl -X POST http://localhost:3500/api/products \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{"name":"New Product","price":99.99,"stock":10}'
```

---

## **🖥️ UI Demo (Next.js)**

The **RDBMS UI Demo** provides a visual interface for interacting with the MiniDB through the REST API.

### **Features**

* Login & session handling
* Role-aware navigation
* Product management
* Admin-only user management
* Read-only views for viewers

### **Role-Based UI Behavior**

| Role    | UI Access                |
| ------- | ------------------------ |
| Admin   | Users, roles, products   |
| Manager | Products (create/update) |
| User    | View products            |
| Viewer  | Read-only                |

---


### **UI Project Structure**

```
rdbms-ui-demo/
├── app/
│   ├── login/
│   ├── dashboard/
│   ├── products/
│   └── users/
├── components/
├── lib/
│   └── api.ts
├── middleware.ts
└── package.json
```

---

## **📁 Project Structure (Full System)**

```
pesapal/
├── pesapal-rdbms/     # MiniDB engine
├── api/               # REST API
├── rdbms-ui-demo/     # Next.js UI
└── README.md
```

---


## **🔍 Health Checks**

```bash
# MiniDB
curl http://localhost:2500/health

# API
curl http://localhost:3500/health
```

---

## **⚙️ Configuration**

### **Ports**

* MiniDB: **2500**
* API: **3500**
* UI: **3000**

### **API Environment Variables**

`/.env`

```env
MINIDB_URL=http://localhost:2500
SECRET_KEY=your-secret-key-here
DEBUG=True
```

---

## **🎯 System Flow**

1. **MiniDB** handles storage & SQL execution
2. **REST API** enforces authentication and RBAC
3. **Seeder** initializes the system
4. **UI** consumes the API and enforces permissions visually

---

## **📞 Support & Tooling**

* API Docs: [http://localhost:3500](http://localhost:3500)
* MiniDB Shell: `python main.py`
* UI: [http://localhost:3000/auth/login](http://localhost:3000/auth/login)
* Postman / cURL supported

---

