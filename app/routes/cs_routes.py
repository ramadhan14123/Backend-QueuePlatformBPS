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
    """
    Konfirmasi kunjungan berdasarkan visit_id
    ---
    tags:
      - Customer Service
    parameters:
      - name: visit_id
        in: path
        type: integer
        required: true
        description: ID kunjungan yang akan dikonfirmasi
    responses:
      200:
        description: Visit confirmed successfully
      401:
        description: Unauthorized action
      404:
        description: Visit not found
    """
    return confirm_visit(visit_id)

@cs_bp.route('/reset', methods=['POST'])
@jwt_required_custom
def reset():
    """
    Reset antrian secara manual
    ---
    tags:
      - Customer Service
    responses:
      200:
        description: Antrian berhasil direset
      401:
        description: Unauthorized action
    """
    return manual_reset_queue()

@cs_bp.route('/login', methods=['POST'])
def login():
    """
    Login admin/CS
    ---
    tags:
      - Customer Service
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              admin:
                type: string
              password:
                type: string
    responses:
      200:
        description: Login berhasil
      401:
        description: Login gagal
    """
    return cs_login()

@cs_bp.route('/resetdb', methods=['POST'])
@jwt_required_custom
def reset_db():
    """
    Reset database secara manual
    ---
    tags:
      - Customer Service
    responses:
      200:
        description: Database berhasil direset
      401:
        description: Unauthorized action
    """
    return manual_reset_db()

@cs_bp.route('/reset-countdown', methods=['GET'])
def countdown():
    """
    Reset countdown antrian
    ---
    tags:
      - Customer Service
    responses:
      200:
        description: Countdown berhasil direset
    """
    return reset_countdown()

@cs_bp.route('/actlogs', methods=['GET'])
# @jwt_required_custom
def fetch_logs():
    """
    Ambil data log aktivitas admin
    ---
    tags:
      - Customer Service
    responses:
      200:
        description: Data log aktivitas admin
    """
    return get_logs()

@cs_bp.route('/expiredLogs', methods=['POST'])
# @jwt_required_custom
def set_log_expiry_days_route():
    """
    Set waktu kadaluarsa log aktivitas admin (dalam hari)
    ---
    tags:
      - Customer Service
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              days:
                type: integer
                description: Jumlah hari sebelum log kadaluarsa
    responses:
      200:
        description: Waktu kadaluarsa log berhasil diatur
      400:
        description: Input tidak valid
    """
    return set_default_log_expiry(request.get_json())

@cs_bp.route('/get-expired-logs', methods=['GET'])
def get_expired_logs():
    """
    Ambil pengaturan waktu kadaluarsa log aktivitas admin
    ---
    tags:
      - Customer Service
    responses:
      200:
        description: Pengaturan waktu kadaluarsa log
    """
    return get_log_expiry_days()