from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
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
def generate_token():
    token = get_access_token()
    return token

@payments_bp.route("/test-password")
def test_password():
    return generate_stk_password()

@payments_bp.route("/callback", methods=["POST"])
def stk_callback():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    print("STK CALLBACK RECEIVED:")
    print(data)

    return {"ResultCode": 0, "ResultDesc": "Received successfully"}

@payments_bp.route("/stk-push", methods=["POST"])
@jwt_required()
def stk_push():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    phone = data.get("phone")
    amount = data.get("amount")

    if not phone or not amount:
        return jsonify({"error": "Phone and amount required"}), 400

    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a number"}), 400

    if amount_value <= 0:
        return jsonify({"error": "Amount must be greater than zero"}), 400

    response = initiate_stk_push(phone, amount_value)

    return jsonify(response)
