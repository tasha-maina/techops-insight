from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Customer
from flask_jwt_extended import jwt_required, get_jwt


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["POST"])
@jwt_required()
def create_customer():
    data = request.get_json()

    company_name = data.get("company_name")
    contact_email = data.get("contact_email")

    if not company_name or not contact_email:
        return jsonify({"error": "All fields required"}), 400

    customer = Customer(
        company_name=company_name,
        contact_email=contact_email
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "Customer created"}), 201


@customers_bp.route("", methods=["GET"])
@jwt_required()
def get_customers():
    claims = get_jwt()
    print("JWT CLAIMS:", claims)
    customers = Customer.query.all()

    result = []
    for customer in customers:
        result.append({
            "id": customer.id,
            "company_name": customer.company_name,
            "contact_email": customer.contact_email,
            "status": customer.status
        })

    return jsonify(result), 200

@customers_bp.route("/<int:customer_id>", methods=["GET"])
@jwt_required()
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    return jsonify({
        "id": customer.id,
        "company_name": customer.company_name,
        "contact_email": customer.contact_email,
        "status": customer.status
    }), 200

@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@jwt_required()
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()

    customer.company_name = data.get("company_name", customer.company_name)
    customer.contact_email = data.get("contact_email", customer.contact_email)
    customer.status = data.get("status", customer.status)

    db.session.commit()

    return jsonify({"message": "Customer updated"}), 200

@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@jwt_required()
def delete_customer(customer_id):
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403
   
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200