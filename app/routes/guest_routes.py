from flask import Blueprint
from app.controllers.guest_controller import create_guest_visit, get_guest

guest_bp = Blueprint('guest', __name__)

@guest_bp.route('/form', methods=['POST'])
def register_guest():
    return create_guest_visit()

@guest_bp.route('/<int:guest_id>', methods=['GET'])
def get_guestname(guest_id):
    return get_guest(guest_id)