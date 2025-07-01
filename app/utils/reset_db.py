from app.models.visit import Visit
from app.utils.export_utils import export_visits_to_excel
from datetime import datetime
from app.extensions import db
import os

def reset_database(export_format='excel'):
    visits = Visit.query.all()
    output = export_visits_to_excel(visits)
    filename = f"visits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    os.makedirs("exports", exist_ok=True)
    with open(f"exports/{filename}", "wb") as f:
        f.write(output.read())
    Visit.query.delete()
    db.session.commit()
    return filename