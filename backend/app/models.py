from .extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="support")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)

    # General customer state
    status = db.Column(db.String(50), default="active")

    # Subscription state (for payments)
    subscription_status = db.Column(
        db.String(50),
        default="inactive"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Customer {self.company_name}>"
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    amount = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    mpesa_receipt = db.Column(db.String(100), nullable=True)

    checkout_request_id = db.Column(
        db.String(100),
        nullable=True
    )

    status = db.Column(
        db.String(50),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    customer = db.relationship(
        "Customer",
        backref=db.backref("transactions", lazy=True)
    )

    def __repr__(self):
        return f"<Transaction {self.id} - {self.status}>"