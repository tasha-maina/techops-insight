import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models import Customer, Transaction

class PaymentsTestCase(unittest.TestCase):
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
            self.customer_id = customer.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_transactions_empty(self):
        with self.app.app_context():
            response = self.client.get("/payments/transactions", headers={})
            self.assertEqual(response.status_code, 401)

    def test_payment_validation_without_customer_id(self):
        with self.app.app_context():
            response = self.client.post(
                "/payments/stk-push",
                json={"phone": "254700000000", "amount": 100}
            )
            self.assertEqual(response.status_code, 401)

    def test_invalid_customer_id_type(self):
        with self.app.app_context():
            response = self.client.post(
                "/payments/stk-push",
                json={"customer_id": "abc", "phone": "254700000000", "amount": 100},
                headers={}
            )
            self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
