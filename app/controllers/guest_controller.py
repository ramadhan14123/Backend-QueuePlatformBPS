from flask import request, jsonify
from app.extensions import db
from app.models.guest import Guest
from app.models.visit import Visit
from app.utils.queue_number import assign_queue_number
from app.utils.email_checker import is_disposable_email
from app.utils.auth import get_current_admin_id
from app.models.log import Log  # Jika ingin mencatat log

def create_guest_visit():
    data = request.json

    # Tolak jika email termasuk disposable/temp mail
    if is_disposable_email(data['email']):
        return jsonify({'error': 'Temporary or disposable email addresses are not allowed.'}), 400

    guest = Guest(
        email=data['email'],
        guest_name=data['guest_name'],
        gender=data['gender'],
        identity_type=data['identity_type'],
        identity_number=data['identity_number'],
        institution=data['institution'],
        phone=data['phone']
    )
    db.session.add(guest)
    db.session.commit()

    if data.get('target_service', '').lower() == 'pelayanan statistik terpadu':
        queue_number = assign_queue_number()
    else:
        queue_number = None

    visit = Visit(
        guest_id=guest.guest_id,
        purpose=data['purpose'],
        target_service=data['target_service'],
        queue_number=queue_number
    )
    db.session.add(visit)
    db.session.commit()

    response = {
        'message': 'Guest and visit created successfully',
        'guest_id': guest.guest_id,
        'visit_id': visit.visit_id
    }
    if queue_number is not None:
        response['queue_number'] = queue_number

    return jsonify(response), 201

def get_all_guests():
    guest = Guest.query.all()
    result = []
    for g in guest:
        result.append({
            'guest_id': g.guest_id,
            'email': g.email,
            'guest_name': g.guest_name,
            'gender':g.gender,
            'identity_type': g.identity_type,
            'identity_number': g.identity_number,
            'institution': g.institution,
            'phone': g.phone
        })
    return jsonify(result), 200


def get_guest(guest_id):
    guest = Guest.query.get(guest_id)
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    return jsonify({
        'guest_id': guest.guest_id,
        'email': guest.email,
        'guest_name': guest.guest_name,
        'gender': guest.gender,
        'identity_type': guest.identity_type,
        'identity_number': guest.identity_number,
        'institution': guest.institution,
    })


def delete_guest(guest_id):
    admin_id = get_current_admin_id()
    if admin_id is None:
        return jsonify({'error': 'Unauthorized action'}), 403

    guest = Guest.query.get(guest_id)
    if not guest:
        return jsonify({'error': 'Guest not found'}), 404
    db.session.delete(guest)
    db.session.commit()

    if str(admin_id) == 'default_admin':
        db.session.add(Log(admin_env='default_admin', action=f"Delete Guest {guest_id}"))
    else:
        db.session.add(Log(admin_id=admin_id, action=f"Delete Guest {guest_id}"))
    db.session.commit()

    return jsonify({'message': 'Guest deleted successfully'}), 200