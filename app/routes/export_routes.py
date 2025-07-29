from flask import Blueprint
from app.controllers.export_controller import export_guest_excel, export_excel, export_logs, list_weekly_exports, download_weekly_export, delete_weekly_export
from app.utils.auth import jwt_required_custom
export_bp = Blueprint('export', __name__)

@export_bp.route('/')
def index():
    return {'status': 'export routes are Activate'}, 200

# Export data guest ke Excel
@export_bp.route('/guest', methods=['GET'])
@jwt_required_custom
def export_guest_excel_route():
    return export_guest_excel()

# Weekly Auto Exports: List, Download, Delete
@export_bp.route('/weekly-auto-exports', methods=['GET'])
@jwt_required_custom
def list_weekly_exports_route():
    return list_weekly_exports()

@export_bp.route('/weekly-download-exports/<filename>', methods=['GET'])
@jwt_required_custom
def download_weekly_export_route(filename):
    return download_weekly_export(filename)

@export_bp.route('/weekly-delete-exports/<filename>', methods=['DELETE'])
@jwt_required_custom
def delete_weekly_export_route(filename):
    return delete_weekly_export(filename)

# Export data visit ke Excel
@export_bp.route('/visit', methods=['GET'])
@jwt_required_custom
def export_visit_excel_route():
    return export_excel()

# (Opsional) Export log ke Excel/PDF
@export_bp.route('/logs', methods=['GET'])
@jwt_required_custom
def export_logs_route():
    return export_logs()