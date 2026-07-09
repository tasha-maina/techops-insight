import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models import Customer, Transaction

class AnalyticsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "test-secret",
            "SECRET_KEY": "test-secret"
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            customer = Customer(company_name="Test Company", contact_email="test@example.com")
            db.session.add(customer)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_access_token(self):
        payload = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "testing123"
        }

        register = self.client.post(
            "/auth/register",
            json=payload
        )
        self.assertEqual(register.status_code, 201)

        login = self.client.post(
            "/auth/login",
            json={
                "email": payload["email"],
                "password": payload["password"]
            }
        )
        self.assertEqual(login.status_code, 200)
        data = login.get_json()
        self.assertIn("access_token", data)
        return data["access_token"]

    def test_analytics_requires_auth(self):
        response = self.client.get("/analytics/summary")
        self.assertEqual(response.status_code, 401)

    def test_analytics_summary_with_token(self):
        token = self._get_access_token()

        with self.app.app_context():
            customer2 = Customer(company_name="Another Company", contact_email="another@example.com", status="inactive", subscription_status="inactive")
            db.session.add(customer2)
            db.session.flush()
            transaction = Transaction(
                customer_id=customer2.id,
                amount=250.00,
                phone_number="254700000001",
                status="success"
            )
            db.session.add(transaction)
            db.session.commit()

        response = self.client.get(
            "/analytics/summary",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total_customers"], 2)
        self.assertEqual(data["successful_transactions"], 1)
        self.assertEqual(data["failed_transactions"], 0)
        self.assertEqual(data["pending_transactions"], 0)
        self.assertEqual(data["successful_amount"], 250.0)

if __name__ == "__main__":
    unittest.main()
