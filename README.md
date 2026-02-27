# 🚀 TechOps Insight

TechOps Insight is a full-stack SaaS-style Customer Operations and Subscription Management Platform designed for service businesses and tech support teams.

The platform provides secure authentication, role-based access control, customer management, analytics, and M-Pesa payment integration via Safaricom Daraja API.

## 🎯 Project Vision

TechOps Insight is built to simulate a real world production SaaS system with:

- Secure authentication & authorization
- Customer lifecycle management
- Subscription billing
- Payment processing (M-Pesa STK Push)
- Analytics dashboard
- Admin controls
- Modular backend architecture
- Modern frontend dashboard

This project demonstrates real-world backend engineering principles and API integrations.

## 🛠 Tech Stack

### Backend
- Python 3.12
- Flask (App Factory Pattern)
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Bcrypt (password hashing)

### Frontend
- React
- Axios
- JWT based authentication
- Role based UI rendering
- Dashboard interface

### Payments
- Safaricom Daraja API
- M-Pesa STK Push
- Callback handling
- Payment verification
- Subscription activation logic

## 🔐 Core Features

### 1️⃣ Authentication & Security
- User registration
- Login with JWT access tokens
- Password hashing with bcrypt
- Role-based access control (Admin / Support)
- Protected API routes

### 2️⃣ Customer Management (CRUD)
- Create customers
- View customers
- Update customers
- Delete customers (Admin only)
- Status tracking
- Subscription status control

### 3️⃣ Role-Based Authorization
- Admin-only actions (delete, create restricted)
- Role stored inside JWT custom claims
- Claims verified on protected routes

### 4️⃣ Payments (M-Pesa Integration)
- STK Push initiation
- OAuth token generation
- Daraja password encoding
- Payment callback endpoint
- Transaction status tracking
- Automatic subscription activation

### 5️⃣ Analytics 
- Customer activity tracking
- Subscription metrics
- Revenue insights
- Dashboard statistics

## 📂 Project Structure


techops-insight/
│
├── backend/
│ ├── app/
│ │ ├── auth/
│ │ ├── customers/
│ │ ├── payments/
│ │ ├── analytics/
│ │ ├── models.py
│ │ ├── extensions.py
│ │ └── init.py
│ │
│ ├── migrations/
│ ├── config.py
│ ├── run.py
│ └── requirements.txt
│
└── frontend/ (Planned)

## 🔌 API Endpoints

### Authentication

POST /auth/register
POST /auth/login


### Customers

GET /customers
POST /customers
GET /customers/<id>
PUT /customers/<id>
DELETE /customers/<id> (Admin Only)


### Payments (Planned)

POST /payments/stk
POST /payments/callback
GET /payments/status/<transaction_id>

## ⚙️ Installation (Backend)

1. Clone repository

git clone https://github.com/tasha-maina/techops-insight.git

cd techops-insight/backend


2. Create virtual environment

python3 -m venv venv
source venv/bin/activate


3. Install dependencies

pip install -r requirements.txt


4. Configure PostgreSQL database in `config.py`

5. Run migrations

flask db upgrade


6. Start server

python run.py

## 💰 M-Pesa Integration Architecture (Design Overview)

1. User initiates payment from frontend
2. Backend generates OAuth token (Daraja)
3. Backend sends STK Push request
4. User receives payment prompt on phone
5. Safaricom sends callback to backend
6. Backend verifies transaction
7. Subscription status updated in database

## 🧠 Engineering Principles Demonstrated

- Modular Flask architecture
- App factory pattern
- Blueprint separation
- JWT identity & custom claims
- Role-based route enforcement
- RESTful API design
- PostgreSQL migrations
- External API integration (Daraja)
- Secure credential handling
- Environment-based configuration

## 🚀 Future Enhancements

- Docker containerization
- CI/CD with GitHub Actions
- Deployment to cloud (Render / Railway)
- Unit and integration tests
- Email notifications
- Admin analytics dashboard
- Subscription renewal automation

## 👩🏽‍💻 Author

Tasha Maina  
Full Stack Developer  
GitHub: https://github.com/tasha-maina
