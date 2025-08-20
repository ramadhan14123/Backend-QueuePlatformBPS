from flask import Blueprint
from app.controllers.export_controller import export_guest_excel, export_excel, export_logs, list_weekly_exports, download_weekly_export, delete_weekly_export
from app.utils.auth import jwt_required_custom
export_bp = Blueprint('export', __name__)

@export_bp.route('/')
def index():
    """
    Cek status route export
    ---
    tags:
      - Export
    responses:
      200:
        description: Route export aktif
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: export routes are Activate
    """
    return {'status': 'export routes are Activate'}, 200

# Export data guest ke Excel
@export_bp.route('/guest', methods=['GET'])
@jwt_required_custom
def export_guest_excel_route():
    """
    Export data tamu ke file Excel
    ---
    tags:
      - Export
    responses:
      200:
        description: File Excel tamu (.xlsx)
        content:
          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
            schema:
              type: string
              format: binary
      401:
        description: Tidak terautentikasi
      500:
        description: Terjadi kesalahan server
    """
    return export_guest_excel()

# Weekly Auto Exports: List, Download, Delete
@export_bp.route('/weekly-auto-exports', methods=['GET'])
@jwt_required_custom
def list_weekly_exports_route():
    """
    Menampilkan daftar file export mingguan yang tersedia
    ---
    tags:
      - Export
    responses:
      200:
        description: Daftar file export mingguan (JSON)
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  filename:
                    type: string
                  size:
                    type: integer
                  modified:
                    type: number
      401:
        description: Tidak terautentikasi
    """
    return list_weekly_exports()

@export_bp.route('/weekly-download-exports/<filename>', methods=['GET'])
@jwt_required_custom
def download_weekly_export_route(filename):
    """
    Download file export mingguan berdasarkan nama file
    ---
    tags:
      - Export
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Nama file yang akan diunduh
    responses:
      200:
        description: File berhasil diunduh (.xlsx)
        content:
          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
            schema:
              type: string
              format: binary
      401:
        description: Tidak terautentikasi
      404:
        description: File tidak ditemukan
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: File not found
    """
    return download_weekly_export(filename)

@export_bp.route('/weekly-delete-exports/<filename>', methods=['DELETE'])
@jwt_required_custom
def delete_weekly_export_route(filename):
    """
    Hapus file export mingguan berdasarkan nama file
    ---
    tags:
      - Export
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Nama file yang akan dihapus
    responses:
      200:
        description: File berhasil dihapus
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: File deleted
      401:
        description: Tidak terautentikasi
      404:
        description: File tidak ditemukan
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: File not found
    """
    return delete_weekly_export(filename)

# Export data visit ke Excel
@export_bp.route('/visit', methods=['GET'])
@jwt_required_custom
def export_visit_excel_route():
    """
    Export data kunjungan ke file Excel
    ---
    tags:
      - Export
    responses:
      200:
        description: File Excel kunjungan (.xlsx)
        content:
          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
            schema:
              type: string
              format: binary
      401:
        description: Tidak terautentikasi
      500:
        description: Terjadi kesalahan server
    """
    return export_excel()

# (Opsional) Export log ke Excel/PDF
@export_bp.route('/logs', methods=['GET'])
@jwt_required_custom
def export_logs_route():
    """
    Export data log admin ke file Excel
    ---
    tags:
      - Export
    responses:
      200:
        description: File Excel log admin (.xlsx)
        content:
          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
            schema:
              type: string
              format: binary
      401:
        description: Tidak terautentikasi
      500:
        description: Terjadi kesalahan server
    """
    return export_logs()