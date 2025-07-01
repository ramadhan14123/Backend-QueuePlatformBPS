from flask import Blueprint
from app.controllers.cs_controller import confirm_visit, manual_reset_queue, cs_login, get_logs, reset_countdown
from flask_jwt_extended import jwt_required as jqwt_required
from app.controllers.cs_controller import manual_reset_db

cs_bp = Blueprint('cs', __name__)

@cs_bp.route('/')
def index():
    return {'status': 'cs routes are Activate'}, 200

@cs_bp.route('/confirm', methods=['POST'])
@jqwt_required()
def confirm_visit_route():
    return confirm_visit()

@cs_bp.route('/reset', methods=['POST'])
@jqwt_required()
def reset():
    return manual_reset_queue()

@cs_bp.route('/login', methods=['POST'])
def login():
    return cs_login()

@cs_bp.route('/resetdb', methods=['POST'])
@jqwt_required()
def reset_db():
    return manual_reset_db()

@cs_bp.route('/reset-countdown', methods=['GET'])
def countdown():
    return reset_countdown()

@cs_bp.route('/actlogs', methods=['GET'])
@jqwt_required()
def fetch_logs():
    """
    Fetch logs from the database.
    """
    return get_logs()