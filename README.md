# 🚀 TechOps Insight

TechOps Insight is a customer operations dashboard with secure authentication, customer management, M-Pesa payment integration, and analytics.

This repository contains a Flask backend API and a static frontend served from the root-level `frontend/` directory.

## 🧩 What’s included

- Backend API in `backend/`
- Static frontend in `frontend/`
- JWT authentication
- Customer CRUD operations
- M-Pesa Daraja STK Push payment flows
- Transaction persistence and callback handling
- Analytics summary endpoint
- Unit tests for backend behavior

## ⚙️ Setup

1. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Create `backend/.env` with:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DARAJA_CONSUMER_KEY=your-daraja-key
DARAJA_CONSUMER_SECRET=your-daraja-secret
DARAJA_BASE_URL=https://sandbox.safaricom.co.ke
DARAJA_SHORTCODE=123456
DARAJA_PASSKEY=your-passkey
DARAJA_CALLBACK_URL=https://yourdomain.com/payments/callback
```

4. Run database migrations:

```bash
cd backend
flask db upgrade
```

5. Start the app from the repository root:

```bash
cd /home/dmintasha/techops-insight
.venv/bin/python backend/run.py
```

6. Open the frontend in your browser:

```text
http://127.0.0.1:5001/
```

## 📚 API Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Customers
- `GET /customers`
- `POST /customers`
- `GET /customers/<id>`
- `PUT /customers/<id>`
- `DELETE /customers/<id>`

### Payments
- `GET /payments/health`
- `GET /payments/token`
- `GET /payments/test-password`
- `GET /payments/transactions`
- `POST /payments/stk-push`
- `POST /payments/callback`

### Analytics
- `GET /analytics/summary`

## 🧪 Tests

Run backend tests from the repository root:

```bash
cd backend
python -m unittest discover tests
```

## 📁 Project Layout

```
techops-insight/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
└── frontend/
    └── index.html
```

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

Natasha Maina  
Full Stack Developer  
GitHub: https://github.com/tasha-maina
>>>>>>> origin/main
