from app.extensions import db
from flask import send_file, request
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
    output = export_visits_to_excel(visits)  # langsung pakai fungsi dari utils
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='kunjungan.xlsx',
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )