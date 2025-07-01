import pandas as pd
from io import BytesIO
import io

def export_visits_to_excel(visits):
    data = [{
        "visit_id": v.visit_id,
        "guest_id": v.guest_id,
        "purpose": v.purpose,
        "target_service": v.target_service,
        "timestamp": v.timestamp,
        "queue_number": v.queue_number,
        "mark": v.mark
    } for v in visits]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

def export_logs_to_excel(logs):
    df = pd.DataFrame([{
        'admin_id': log.admin_id,
        'Timestamp': log.timestamp,
        'Action': log.action
    } for log in logs])
    
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

def export_guests_to_excel(guests):
    data = [{
        "guest_id": g.guest_id,
        "guest_name": g.guest_name,
        "email": g.email,
        "gender": g.gender,
        "identity_type": g.identity_type,
        "identity_number": g.identity_number,
        "institution": g.institution,
        "phone": g.phone
    } for g in guests]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output
