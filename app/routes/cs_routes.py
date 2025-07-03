from flask import Blueprint
from app.controllers.cs_controller import confirm_visit, manual_reset_queue, cs_login, get_logs, reset_countdown
from app.utils.auth import jwt_required_custom
from app.controllers.cs_controller import manual_reset_db

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
@jwt_required_custom
def fetch_logs():
    """
    Fetch logs from the database.
    """
    return get_logs()