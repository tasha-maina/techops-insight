# TechOps Insight Backend

This repository contains the backend API for TechOps Insight, a Flask application that manages users, customers, and M-Pesa payment transactions.

## Setup

1. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Create a `.env` file in the `backend` folder with the required variables:

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

5. Start the application from the repository root:

```bash
cd /home/dmintasha/techops-insight
.venv/bin/python backend/run.py
```

Then open the UI in your browser:

```text
http://127.0.0.1:5001/
```

## API Endpoints

### Auth
- `POST /auth/register` — register a new user
- `POST /auth/login` — log in and receive a JWT access token

### Customers
- `POST /customers` — create a customer (JWT required)
- `GET /customers` — list customers (JWT required)
- `GET /customers/<id>` — get a customer
- `PUT /customers/<id>` — update a customer
- `DELETE /customers/<id>` — delete a customer (admin only)

### Payments
- `GET /payments/health` — check payments module readiness
- `GET /payments/token` — generate Daraja access token (JWT required)
- `GET /payments/test-password` — generate STK password (JWT required)
- `GET /payments/transactions` — list transaction records (JWT required)
- `POST /payments/stk-push` — initiate an STK push payment (JWT required)
- `POST /payments/callback` — receive Daraja callback events

### Analytics
- `GET /analytics/summary` — get customer and transaction summary metrics (JWT required)

## Tests

Run tests with:

```bash
cd backend
python -m unittest discover tests
```
