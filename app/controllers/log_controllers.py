from flask import jsonify
from datetime import datetime, timedelta
from app.models.log import Log
from app.extensions import db

DEFAULT_LOG_EXPIRY_DAYS = 7

def set_default_log_expiry(json_data):
    try:
        days = int(json_data.get('days', 7))
    except (KeyError, ValueError, TypeError):
        return jsonify({"status": "error", "message": "Data input tidak valid"}), 400
    global DEFAULT_LOG_EXPIRY_DAYS
    DEFAULT_LOG_EXPIRY_DAYS = days
    return jsonify({"status": "sukses", "pesan": f"Default kadaluarsa log diubah menjadi {days} hari."}), 200

def get_default_log_expiry():
    return DEFAULT_LOG_EXPIRY_DAYS

def create_log(json_data):
    try:
        admin_id = json_data.get('admin_id')
        admin_env = json_data.get('admin_env')
        action = json_data['action']
        days = get_default_log_expiry()
    except (KeyError, ValueError, TypeError):
        return {"status": "error", "message": "Data input tidak valid"}

    timestamp = datetime.utcnow()
    expired_at = timestamp + timedelta(days=days)

    log = Log(
        admin_id=admin_id,
        admin_env=admin_env,
        action=action,
        timestamp=timestamp,
        expired_at=expired_at
    )
    db.session.add(log)
    try:
        db.session.commit()
        return {
            "status": "sukses",
            "log_id": log.log_id,
            "timestamp": timestamp.isoformat(),
            "expired_at": expired_at.isoformat(),
            "pesan": f"Log berhasil dibuat dan akan kadaluarsa dalam {days} hari (default)."
        }
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": f"Gagal membuat log: {str(e)}"}
    
def delete_expired_logs():
    now = datetime.utcnow()
    query = Log.__table__.delete().where(Log.expired_at != None, Log.expired_at < now)
    result = db.session.execute(query)
    db.session.commit()
    count = result.rowcount if hasattr(result, 'rowcount') else None
    return jsonify({"status": "sukses", "deleted": count, "pesan": f"{count} log expired berhasil dihapus."})

def get_log_expiry_days():
    days = get_default_log_expiry()
    return jsonify({"days": days}), 200
