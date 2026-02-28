from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .services import get_access_token
from .services import generate_stk_password


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

    print("STK CALLBACK RECEIVED:")
    print(data)

    return {"ResultCode": 0, "ResultDesc": "Received successfully"}