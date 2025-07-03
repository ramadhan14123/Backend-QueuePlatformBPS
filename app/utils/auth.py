from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

def jwt_required_custom(fn=None, *, fresh=False, optional=False, refresh=False, locations=None):
    def decorator(inner_fn):
        @wraps(inner_fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(fresh=fresh, optional=optional, refresh=refresh, locations=locations)
            except Exception as e:
                return jsonify({"error": "Unauthorized", "message": str(e)}), 401
            return inner_fn(*args, **kwargs)
        return wrapper

    if fn:
        return decorator(fn)
    return decorator

def get_current_admin_id():
    """
    Helper untuk mengambil admin_id dari JWT token.
    """
    identity = get_jwt_identity()
    if identity == 'default_admin':
        return 'default_admin'
    return int(identity)