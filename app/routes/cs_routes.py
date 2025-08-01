from flask import Blueprint, request, jsonify
from app.controllers.cs_controller import confirm_visit, manual_reset_queue, cs_login, get_logs, reset_countdown
from app.controllers.cs_controller import manual_reset_db
from app.utils.auth import jwt_required_custom
from app.controllers.log_controllers import set_default_log_expiry
from app.controllers.log_controllers import get_log_expiry_days


cs_bp = Blueprint('cs', __name__)

@cs_bp.route('/')
def index():
    return {'status': 'cs routes are Activate'}, 200

@cs_bp.route('/confirm/<int:visit_id>', methods=['PUT'])
@jwt_required_custom
def confirm_visit_route(visit_id):
    return confirm_visit(visit_id)

@cs_bp.route('/reset', methods=['POST'])
@jwt_required_custom
def reset():
    return manual_reset_queue()

@cs_bp.route('/login', methods=['POST'])
def login():
    return cs_login()

@cs_bp.route('/resetdb', methods=['POST'])
@jwt_required_custom
def reset_db():
    return manual_reset_db()

@cs_bp.route('/reset-countdown', methods=['GET'])
def countdown():
    return reset_countdown()

@cs_bp.route('/actlogs', methods=['GET'])
# @jwt_required_custom
def fetch_logs():
    return get_logs()

@cs_bp.route('/expiredLogs', methods=['POST'])
# @jwt_required_custom
def set_log_expiry_days_route():
    return set_default_log_expiry(request.get_json())

@cs_bp.route('/get-expired-logs', methods=['GET'])
def get_expired_logs():
    return get_log_expiry_days()