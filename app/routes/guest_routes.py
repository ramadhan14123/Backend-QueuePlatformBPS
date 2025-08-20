from flask import Blueprint
from app.controllers.guest_controller import create_guest_visit, get_guest, delete_guest, get_all_guests
from app.utils.auth import jwt_required_custom

guest_bp = Blueprint('guest', __name__)

@guest_bp.route('/allguest', methods=['GET'])
@jwt_required_custom
def all_guests():
    """
    Mendapatkan seluruh data tamu
    ---
    tags:
      - Guest
    responses:
      200:
        description: Daftar seluruh tamu
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  guest_id:
                    type: integer
                  email:
                    type: string
                  guest_name:
                    type: string
                  gender:
                    type: string
                  identity_type:
                    type: string
                  identity_number:
                    type: string
                  institution:
                    type: string
                  phone:
                    type: string
    """
    return get_all_guests()

@guest_bp.route('/form', methods=['POST'])
def register_guest():
    """
    Registrasi kunjungan tamu baru
    ---
    tags:
      - Guest
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "user@email.com"
            guest_name:
              type: string
              example: "Budi"
            gender:
              type: string
              enum: ["L", "P"]
              example: "L"
            identity_type:
              type: string
              example: "KTP"
            identity_number:
              type: string
              example: "1234567890"
            institution:
              type: string
              example: "Universitas Muhammadiyah Sidoarjo"
            phone:
              type: string
              example: "08123456789"
            purpose:
              type: string
              example: "Konsultasi"
            target_service:
              type: string
              example: "Pelayanan Statistik Terpadu"
    responses:
      201:
        description: Tamu dan kunjungan berhasil dibuat
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Guest and visit created successfully
                guest_id:
                  type: integer
                  example: 1
                visit_id:
                  type: integer
                  example: 1
                queue_number:
                  type: string
                  example: "A001"
      400:
        description: Email sementara tidak diperbolehkan atau input tidak valid
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Temporary or disposable email addresses are not allowed.
    """
    return create_guest_visit()

@guest_bp.route('/<int:guest_id>', methods=['GET'])
def get_guestname(guest_id):
    """
    Mendapatkan data tamu berdasarkan ID
    ---
    tags:
      - Guest
    parameters:
      - name: guest_id
        in: path
        type: integer
        required: true
        description: ID dari tamu
    responses:
      200:
        description: Data tamu ditemukan
        content:
          application/json:
            schema:
              type: object
              properties:
                guest_id:
                  type: integer
                email:
                  type: string
                guest_name:
                  type: string
                gender:
                  type: string
                identity_type:
                  type: string
                identity_number:
                  type: string
                institution:
                  type: string
                status:
                  type: string
                  nullable: true
      404:
        description: Guest not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Guest not found
    """
    return get_guest(guest_id)

@guest_bp.route('/<int:guest_id>', methods=['DELETE'])
@jwt_required_custom
def delete_guest_route(guest_id):
    """
    Hapus tamu berdasarkan ID
    ---
    tags:
      - Guest
    parameters:
      - name: guest_id
        in: path
        type: integer
        required: true
        description: ID dari tamu
    responses:
      200:
        description: Tamu berhasil dihapus
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Guest deleted successfully
      404:
        description: Tamu tidak ditemukan
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Guest not found
      403:
        description: Unauthorized action
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Unauthorized action
    """
    return delete_guest(guest_id)