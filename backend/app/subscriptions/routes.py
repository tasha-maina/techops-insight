from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from ..extensions import db
from ..models import Customer
from ..emails import send_email

subscriptions_bp = Blueprint("subscriptions", __name__, url_prefix="/subscriptions")


@subscriptions_bp.route("/renewals/process", methods=["POST"])
@jwt_required()
def process_subscription_renewals():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    now = datetime.utcnow()
    due_customers = Customer.query.filter(
        Customer.subscription_status == "active",
        Customer.next_renewal_date != None,
        Customer.next_renewal_date <= now
    ).all()

    results = []
    for customer in due_customers:
        customer.next_renewal_date = now + timedelta(days=30)
        db.session.add(customer)
        results.append({
            "id": customer.id,
            "company_name": customer.company_name,
            "contact_email": customer.contact_email,
            "next_renewal_date": customer.next_renewal_date.isoformat()
        })

        if current_app.config.get("EMAIL_ENABLED"):
            send_email(
                to_address=customer.contact_email,
                subject="Subscription renewal processed",
                body=(
                    f"Hello {customer.company_name},\n\n"
                    "Your subscription has been renewed successfully. "
                    "Your next renewal date is "
                    f"{customer.next_renewal_date.isoformat()}.\n\n"
                    "Thank you for using TechOps Insight."
                )
            )

    db.session.commit()

    return jsonify({
        "renewed_customers": results,
        "total": len(results)
    }), 200
