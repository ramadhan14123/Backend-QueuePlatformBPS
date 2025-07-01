from flask import Blueprint
from app.controllers.visit_controller import get_visits, create_visit, update_visit, category_visits_logic as category_visits_logic

visit_bp = Blueprint('visit', __name__)

@visit_bp.route('/')
def index():
    return {'status': 'Visit routes are Activate'}, 200

@visit_bp.route('/visits', methods=['GET'])
def visits_get():
    return get_visits()

@visit_bp.route('/visits', methods=['POST'])
def visits_post():
    return create_visit()

@visit_bp.route('/visits/<int:visit_id>', methods=['PUT'])
def visits_put(visit_id):
    return update_visit(visit_id)

@visit_bp.route('/category', methods=['GET'])
def category_visits():
    return category_visits_logic()