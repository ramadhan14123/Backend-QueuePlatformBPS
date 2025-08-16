from app.extensions import db
from flask import send_file, request, jsonify, send_from_directory, make_response
import os
from app.models.visit import Visit
from app.models.log import Log
from app.utils.export_utils import export_visits_to_excel, export_logs_to_excel, export_guests_to_excel
from app.models.guest import Guest

def export_guest_excel():
    guests = Guest.query.all()
    output = export_guests_to_excel(guests)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='guest.xlsx',
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def export_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    output = export_logs_to_excel(logs)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='log_admin.xlsx',
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def export_excel():
    visits = Visit.query.all()
    output = export_visits_to_excel(visits)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name='kunjungan.xlsx',
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

EXPORTS_FOLDER = os.path.join(os.getcwd(), 'exports')

# List all weekly auto export files
def list_weekly_exports():
    files = []
    for fname in os.listdir(EXPORTS_FOLDER):
        fpath = os.path.join(EXPORTS_FOLDER, fname)
        if os.path.isfile(fpath):
            stat = os.stat(fpath)
            files.append({
                'filename': fname,
                'size': stat.st_size,
                'modified': stat.st_mtime
            })
    return jsonify(sorted(files, key=lambda x: x['modified'], reverse=True))

# Download a specific export file
def download_weekly_export(filename):
    return send_from_directory(EXPORTS_FOLDER, filename, as_attachment=True)

# Delete a specific export file
def delete_weekly_export(filename):
    fpath = os.path.join(EXPORTS_FOLDER, filename)
    if os.path.exists(fpath):
        os.remove(fpath)
        return jsonify({'message': 'File deleted'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404