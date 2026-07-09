from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Transaction, Customer
from .services import get_access_token
from .services import generate_stk_password
from .services import initiate_stk_push


payments_bp = Blueprint(
    "payments",
    __name__,
    url_prefix="/payments"
)


@payments_bp.route("/health", methods=["GET"])
@jwt_required()
def payments_health():
    return jsonify({"message": "Payments module ready"}), 200


@payments_bp.route("/token")
@jwt_required()
def generate_token():
    token = get_access_token()
    return jsonify({"access_token": token})


@payments_bp.route("/test-password")
@jwt_required()
def test_password():
    return jsonify(generate_stk_password())


@payments_bp.route("/transactions", methods=["GET"])
@jwt_required()
def list_transactions():
    customer_id = request.args.get("customer_id")
    query = Transaction.query.order_by(Transaction.created_at.desc())

    if customer_id is not None:
        try:
            customer_id_value = int(customer_id)
            query = query.filter_by(customer_id=customer_id_value)
        except (TypeError, ValueError):
            return jsonify({"error": "customer_id must be an integer"}), 400

    transactions = query.all()
    return jsonify([
        {
            "id": txn.id,
            "customer_id": txn.customer_id,
            "phone_number": txn.phone_number,
            "amount": float(txn.amount),
            "status": txn.status,
            "checkout_request_id": txn.checkout_request_id,
            "mpesa_receipt": txn.mpesa_receipt,
            "created_at": txn.created_at.isoformat()
        }
        for txn in transactions
    ]), 200


@payments_bp.route("/callback", methods=["POST"])
def stk_callback():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    body = data.get("Body", {})
    stk_callback_data = body.get("stkCallback", {})
    checkout_request_id = stk_callback_data.get("CheckoutRequestID")
    result_code = stk_callback_data.get("ResultCode")
    result_desc = stk_callback_data.get("ResultDesc")

    transaction = None
    if checkout_request_id:
        transaction = Transaction.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()

    if transaction:
        if result_code == 0:
            transaction.status = "success"
            metadata = stk_callback_data.get("CallbackMetadata", {}).get("Item", [])
            if isinstance(metadata, list):
                for item in metadata:
                    if item.get("Name") == "MpesaReceiptNumber":
                        transaction.mpesa_receipt = item.get("Value")
            if transaction.customer:
                transaction.customer.subscription_status = "active"
                transaction.customer.status = "active"
                transaction.customer.next_renewal_date = datetime.utcnow() + timedelta(days=30)
        else:
            transaction.status = "failed"
        db.session.commit()

    return jsonify({
        "ResultCode": 0,
        "ResultDesc": "Received successfully",
        "transaction_id": transaction.id if transaction else None,
        "processed": bool(transaction)
    })


@payments_bp.route("/stk-push", methods=["POST"])
@jwt_required()
def stk_push():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    customer_id = data.get("customer_id")
    phone = data.get("phone")
    amount = data.get("amount")

    if not customer_id or not phone or not amount:
        return jsonify({"error": "customer_id, phone and amount are required"}), 400

    try:
        customer_id_value = int(customer_id)
    except (TypeError, ValueError):
        return jsonify({"error": "customer_id must be an integer"}), 400

    customer = Customer.query.get(customer_id_value)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a number"}), 400

    if amount_value <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    transaction = Transaction(
        customer_id=customer.id,
        amount=amount_value,
        phone_number=phone,
        status="pending"
    )
    db.session.add(transaction)
    db.session.commit()

    response = initiate_stk_push(phone, amount_value)
    checkout_request_id = response.get("CheckoutRequestID")
    if checkout_request_id:
        transaction.checkout_request_id = checkout_request_id
        db.session.commit()

    return jsonify({
        "transaction_id": transaction.id,
        "status": transaction.status,
        "checkout_request_id": transaction.checkout_request_id,
        "payment_response": response
    }), 200
