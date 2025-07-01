from flask import request, jsonify
from app.extensions import db
from app.models.guest import Guest
from app.models.visit import Visit
from app.utils.queue_number import assign_queue_number
from app.utils.email_checker import is_disposable_email

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