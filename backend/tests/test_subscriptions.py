import os
import sys
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db, bcrypt
from app.models import Customer, User


class SubscriptionsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "test-secret",
            "SECRET_KEY": "test-secret",
            "EMAIL_ENABLED": False
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=bcrypt.generate_password_hash("adminpass").decode("utf-8"),
                role="admin"
            )
            support_user = User(
                username="support",
                email="support@example.com",
                password_hash=bcrypt.generate_password_hash("supportpass").decode("utf-8"),
                role="support"
            )
            due_customer = Customer(
                company_name="Renewal Co",
                contact_email="renewal@example.com",
                status="active",
                subscription_status="active",
                next_renewal_date=datetime.utcnow() - timedelta(days=1)
            )
            db.session.add_all([admin, support_user, due_customer])
            db.session.commit()
            self.admin_email = admin.email
            self.support_email = support_user.email

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _login(self, email, password):
        response = self.client.post(
            "/auth/login",
            json={"email": email, "password": password}
        )
        self.assertEqual(response.status_code, 200)
        return response.get_json().get("access_token")

    def test_renewals_process_admin_only(self):
        token = self._login(self.support_email, "supportpass")
        response = self.client.post(
            "/subscriptions/renewals/process",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 403)

    def test_renewals_process_updates_due_subscriptions(self):
        token = self._login(self.admin_email, "adminpass")
        response = self.client.post(
            "/subscriptions/renewals/process",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["renewed_customers"][0]["company_name"], "Renewal Co")

        with self.app.app_context():
            customer = Customer.query.filter_by(contact_email="renewal@example.com").first()
            self.assertIsNotNone(customer.next_renewal_date)
            self.assertGreater(customer.next_renewal_date, datetime.utcnow())


if __name__ == "__main__":
    unittest.main()
