from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
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
