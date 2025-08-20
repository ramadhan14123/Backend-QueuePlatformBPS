from flask import Blueprint
from app.controllers.visit_controller import get_visits, create_visit, update_visit, category_visits_logic as category_visits_logic
from app.utils.auth import jwt_required_custom

visit_bp = Blueprint('visit', __name__)

@visit_bp.route('/')
def index():
    """
    Cek status route Visit
    ---
    tags:
      - Visit
    responses:
      200:
        description: Route visit aktif
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: Visit routes are Activate
    """
    return {'status': 'Visit routes are Activate'}, 200

@visit_bp.route('/GetVisits', methods=['GET'])
def visits_get():
    """
    Mendapatkan seluruh data kunjungan
    ---
    tags:
      - Visit
    responses:
      200:
        description: Daftar seluruh kunjungan
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  visit_id:
                    type: integer
                  guest_id:
                    type: integer
                  purpose:
                    type: string
                  target_service:
                    type: string
                  timestamp:
                    type: string
                  queue_number:
                    type: integer
                    nullable: true
                  mark:
                    type: string
    """
    return get_visits()

@visit_bp.route('/visits', methods=['POST'])
@jwt_required_custom
def visits_post():
    """
    Membuat data kunjungan baru
    ---
    tags:
      - Visit
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            guest_id:
              type: integer
              example: 1
            purpose:
              type: string
              example: "Konsultasi"
            target_service:
              type: string
              example: "pelayanan Statistik Terpadu"
            queue_number:
              type: integer
              example: 1
            mark:
              type: string
              example: "hadir"
    responses:
      201:
        description: Kunjungan berhasil dibuat
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Visit created
                visit_id:
                  type: integer
                  example: 1
      400:
        description: Input tidak valid
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Invalid input
    """
    return create_visit()

@visit_bp.route('/visits/<int:visit_id>', methods=['PUT'])
@jwt_required_custom
def visits_put(visit_id):
    """
    Memperbarui data kunjungan berdasarkan ID
    ---
    tags:
      - Visit
    parameters:
      - name: visit_id
        in: path
        type: integer
        required: true
        description: ID kunjungan yang akan diperbarui
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            mark:
              type: string
              example: "hadir"
            purpose:
              type: string
              example: "Konsultasi"
            target_service:
              type: string
              example: "pelayanan Statistik Terpadu"
    responses:
      200:
        description: Kunjungan berhasil diperbarui
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Visit updated
                visit_id:
                  type: integer
                  example: 1
      404:
        description: Kunjungan tidak ditemukan
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Visit not found
    """
    return update_visit(visit_id)

@visit_bp.route('/category', methods=['GET'])
@jwt_required_custom
def category_visits():
    """
    Mendapatkan data kunjungan yang sudah dikategorikan
    ---
    tags:
      - Visit
    responses:
      200:
        description: Data kunjungan terkelompok per kategori
        content:
          application/json:
            schema:
              type: object
              properties:
                pelayanan Statistik Terpadu:
                  type: array
                  items:
                    type: object
                Kunjungan Dinas:
                  type: array
                  items:
                    type: object
                Lainnya:
                  type: array
                  items:
                    type: object
    """
    return category_visits_logic()