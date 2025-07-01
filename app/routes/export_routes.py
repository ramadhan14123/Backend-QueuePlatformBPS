from flask import Blueprint
from app.controllers.export_controller import export_guest_excel, export_excel, export_logs

export_bp = Blueprint('export', __name__)

@export_bp.route('/')
def index():
    return {'status': 'export routes are Activate'}, 200

# Export data guest ke Excel
@export_bp.route('/guest', methods=['GET'])
def export_guest_excel_route():
    return export_guest_excel()

# Export data visit ke Excel
@export_bp.route('/visit', methods=['GET'])
def export_visit_excel_route():
    return export_excel()

# (Opsional) Export log ke Excel/PDF
@export_bp.route('/logs', methods=['GET'])
def export_logs_route():
    return export_logs()