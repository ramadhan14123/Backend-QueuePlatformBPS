import os
from flask import request, jsonify
from app.extensions import db, bcrypt,scheduler
from datetime import datetime, timedelta
from app.models.visit import Visit
from app.models.cs import CustomerService as CS
from app.models.log import Log
from app.utils.queue_number import reset_queue_number
from app.utils.auth import get_current_admin_id
from flask_jwt_extended import create_access_token
from app.utils.reset_db import reset_database

ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def confirm_visit(visit_id):
    admin_id = get_current_admin_id()
    visit = Visit.query.get(visit_id)
    if not visit:
        return jsonify({'message': 'Visit not found'}), 404
    visit.mark = 'hadir'
    db.session.commit()

    if admin_id is not None:
        if str(admin_id) == 'default_admin':
            db.session.add(Log(admin_env='default_admin', action=f"Confirm Visit {visit_id}"))
        else:
            db.session.add(Log(admin_id=admin_id, action=f"Confirm Visit {visit_id}"))
        db.session.commit()
    return jsonify({'message': 'Visit confirmed successfully'}), 200

def manual_reset_queue():
    admin_id = get_current_admin_id()
    if admin_id is None:
        return jsonify({'error': 'Unauthorized action'}), 403
    reset_queue_number()
    if str(admin_id) == 'default_admin':
        db.session.add(Log(admin_env='default_admin', action="Manual Reset Queue Number"))
    else:
        db.session.add(Log(admin_id=admin_id, action="Manual Reset Queue Number"))
    db.session.commit()
    return jsonify({'message': 'Queue number reset successfully'}), 200

def cs_login():
    data = request.json
    username = data.get('admin')
    password = data.get('password')
    cs = CS.query.filter_by(admin=username).first()
    if cs and bcrypt.check_password_hash(cs.password, password):
        access_token = create_access_token(identity=str(cs.admin_id))
        return jsonify({"token": access_token}), 200

    if username == ADMIN_NAME and password == ADMIN_PASSWORD:
        access_token = create_access_token(identity='default_admin')
        return jsonify({"token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

def manual_reset_db():
    admin_id = get_current_admin_id()
    if admin_id is None:
        return jsonify({'error': 'Unauthorized action'}), 403

    export_format = request.args.get("format", "excel")
    try:
        filename = reset_database(export_format)
        if str(admin_id) == 'default_admin':
            db.session.add(Log(admin_env='default_admin', action=f"Manual Reset DB ({export_format})"))
        else:
            db.session.add(Log(admin_id=admin_id, action=f"Manual Reset DB ({export_format})"))
        db.session.commit()
        return jsonify({'message': f'Database reset successfully, exported to {filename}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def reset_countdown():
    job = scheduler.get_job('weekly_reset')
    if not job or not job.next_run_time:
        return jsonify({'error': 'Job not found or not scheduled'}), 404

    # Kembalikan waktu reset berikutnya dalam format ISO 8601 agar mudah di-parse frontend
    return jsonify({
        'next_reset': job.next_run_time.isoformat()
    })
    
def get_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    result = []
    for log in logs:
        result.append({
            "log_id": log.log_id,
            "admin_id": log.admin_id,
            "admin_env": log.admin_env,
            "action": log.action,
            "timestamp": log.timestamp.isoformat()
        })
    return jsonify(result), 200
