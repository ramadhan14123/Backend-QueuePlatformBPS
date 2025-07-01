from flask import Blueprint, request, jsonify, send_file
from app.models.visit import Visit
from app.extensions import db
from datetime import datetime, timedelta

visit_bp = Blueprint('visit', __name__)

def get_visits():
    visits = Visit.query.order_by(Visit.timestamp.desc()).all()
    result = []
    for visit in visits:
        result.append({
            "visit_id": visit.visit_id,
            "guest_id": visit.guest_id,
            "purpose": visit.purpose,
            "target_service": visit.target_service,
            "timestamp": visit.timestamp.isoformat(),
            "queue_number": visit.queue_number,
            "mark": visit.mark
        })
    return jsonify(result), 200

def create_visit():
    data = request.json
    visit = Visit(
        guest_id=data['guest_id'],
        purpose=data['purpose'],
        target_service=data['target_service'],
        timestamp=datetime.utcnow(),
        queue_number=data.get('queue_number'),
        mark=data.get('mark', 'tidak hadir')
    )
    db.session.add(visit)
    db.session.commit()
    return jsonify({"message": "Visit created", "visit_id": visit.visit_id}), 201

def update_visit(visit_id):
    data = request.json
    visit = Visit.query.get(visit_id)
    if not visit:
        return jsonify({"error": "Visit not found"}), 404

    old_target = visit.target_service

    # Update field 
    if 'mark' in data:
        visit.mark = data['mark']
    if 'purpose' in data:
        visit.purpose = data['purpose']
    if 'target_service' in data:
        visit.target_service = data['target_service']
        if data['target_service'] == "pelayanan Statistik Terpadu":
            last_queue = (
                Visit.query
                .filter_by(target_service="pelayanan Statistik Terpadu")
                .order_by(Visit.queue_number.desc())
                .first()
            )
            visit.queue_number = (last_queue.queue_number + 1) if last_queue and last_queue.queue_number else 1
        elif old_target == "pelayanan Statistik Terpadu":
            visit.queue_number = None
            statistik_visits = (
                Visit.query
                .filter_by(target_service="pelayanan Statistik Terpadu")
                .order_by(Visit.timestamp.asc())
                .all()
            )
            for idx, v in enumerate(statistik_visits, start=1):
                v.queue_number = idx

    db.session.commit()
    return jsonify({"message": "Visit updated", "visit_id": visit.visit_id}), 200

def category_visits_logic():
    visits = Visit.query.order_by(Visit.timestamp.desc()).all()
    categorized = {
        "pelayanan Statistik Terpadu": [],
        "Kunjungan Dinas": [],
        "Lainnya": []
    }
    for visit in visits:
        target = (visit.target_service or "").lower()
        if target == "pelayanan statistik terpadu":
            categorized["pelayanan Statistik Terpadu"].append({
                "visit_id": visit.visit_id,
                "guest_id": visit.guest_id,
                "purpose": visit.purpose,
                "target_service": visit.target_service,
                "timestamp": visit.timestamp.isoformat(),
                "queue_number": visit.queue_number,
                "mark": visit.mark
            })
        elif target == "kunjungan dinas":
            categorized["Kunjungan Dinas"].append({
                "visit_id": visit.visit_id,
                "guest_id": visit.guest_id,
                "purpose": visit.purpose,
                "target_service": visit.target_service,
                "timestamp": visit.timestamp.isoformat(),
                "queue_number": visit.queue_number,
                "mark": visit.mark
            })
        else:
            categorized["Lainnya"].append({
                "visit_id": visit.visit_id,
                "guest_id": visit.guest_id,
                "purpose": visit.purpose,
                "target_service": visit.target_service,
                "timestamp": visit.timestamp.isoformat(),
                "queue_number": visit.queue_number,
                "mark": visit.mark
            })
    return jsonify(categorized), 200

@visit_bp.route('/reset-info', methods=['GET'])
def get_reset_info():
    now = datetime.now()
    next_reset = now + timedelta(days=(7 - now.weekday()))
    next_reset = next_reset.replace(hour=0, minute=0, second=0, microsecond=0)
    return jsonify({
        "next_database_reset": next_reset.isoformat()
    }), 200