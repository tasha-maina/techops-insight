from datetime import datetime, timedelta

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import func
from ..extensions import db
from ..models import Customer, Transaction

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def analytics_summary():
    total_customers = Customer.query.count()
    active_customers = Customer.query.filter_by(status="active").count()
    inactive_customers = Customer.query.filter(Customer.status != "active").count()
    subscription_active = Customer.query.filter_by(subscription_status="active").count()

    total_transactions = Transaction.query.count()
    successful_transactions = Transaction.query.filter_by(status="success").count()
    failed_transactions = Transaction.query.filter_by(status="failed").count()
    pending_transactions = Transaction.query.filter_by(status="pending").count()

    successful_amount = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).filter(Transaction.status == "success").scalar()

    return jsonify({
        "total_customers": total_customers,
        "active_customers": active_customers,
        "inactive_customers": inactive_customers,
        "subscription_active": subscription_active,
        "total_transactions": total_transactions,
        "successful_transactions": successful_transactions,
        "failed_transactions": failed_transactions,
        "pending_transactions": pending_transactions,
        "successful_amount": float(successful_amount)
    }), 200


@analytics_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin_analytics_summary():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    today = datetime.utcnow()
    next_week = today + timedelta(days=7)

    renewal_due = Customer.query.filter(
        Customer.subscription_status == "active",
        Customer.next_renewal_date != None,
        Customer.next_renewal_date <= today
    ).count()

    renewal_soon = Customer.query.filter(
        Customer.subscription_status == "active",
        Customer.next_renewal_date != None,
        Customer.next_renewal_date > today,
        Customer.next_renewal_date <= next_week
    ).count()

    total_customers = Customer.query.count()
    active_customers = Customer.query.filter_by(status="active").count()
    inactive_customers = Customer.query.filter(Customer.status != "active").count()
    subscription_active = Customer.query.filter_by(subscription_status="active").count()

    total_transactions = Transaction.query.count()
    successful_transactions = Transaction.query.filter_by(status="success").count()
    failed_transactions = Transaction.query.filter_by(status="failed").count()
    pending_transactions = Transaction.query.filter_by(status="pending").count()

    successful_amount = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).filter(Transaction.status == "success").scalar()

    renewal_customers = Customer.query.filter(
        Customer.subscription_status == "active",
        Customer.next_renewal_date != None,
        Customer.next_renewal_date <= next_week
    ).order_by(Customer.next_renewal_date.asc()).limit(10).all()

    renewal_list = [
        {
            "id": customer.id,
            "company_name": customer.company_name,
            "contact_email": customer.contact_email,
            "next_renewal_date": customer.next_renewal_date.isoformat() if customer.next_renewal_date else None,
            "status": customer.status,
            "subscription_status": customer.subscription_status
        }
        for customer in renewal_customers
    ]

    return jsonify({
        "total_customers": total_customers,
        "active_customers": active_customers,
        "inactive_customers": inactive_customers,
        "subscription_active": subscription_active,
        "total_transactions": total_transactions,
        "successful_transactions": successful_transactions,
        "failed_transactions": failed_transactions,
        "pending_transactions": pending_transactions,
        "successful_amount": float(successful_amount),
        "renewal_due": renewal_due,
        "renewal_soon": renewal_soon,
        "renewal_customers": renewal_list
    }), 200
