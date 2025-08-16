from flask import Flask
from config import Config
import os
from datetime import datetime, timedelta

from app.extensions import db, migrate, bcrypt, jwt, scheduler
from app.utils.reset_db import reset_database
from app.controllers.log_controllers import delete_expired_logs

def get_next_weekly_reset():
    now = datetime.now()
    next_reset = now + timedelta(days=(7 - now.weekday()))
    next_reset = next_reset.replace(hour=0, minute=0, second=0, microsecond=0)
    return next_reset

def create_app(config_class=Config):
    from app.routes.guest_routes import guest_bp
    from app.routes.visit_routes import visit_bp
    from app.routes.cs_routes import cs_bp
    from app.routes.export_routes import export_bp
    from app.utils.queue_number import reset_queue_number

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(guest_bp, url_prefix='/api/guest')
    app.register_blueprint(visit_bp, url_prefix='/api/visit')
    app.register_blueprint(cs_bp, url_prefix='/api/cs')
    app.register_blueprint(export_bp, url_prefix='/api/export')

    scheduler.add_job(
        func=reset_queue_number,
        trigger="interval",
        seconds=app.config.get('QUEUE_RESET_INTERVAL', 86400),
        id="daily_queue_reset"  
    )

    def reset_database_with_context():
        with app.app_context():
            reset_database(export_format="excel")

    scheduler.add_job(
        func=reset_database_with_context,
        trigger="interval",
        weeks=1, #atur sesuai kebutuhan waktu reset mingguan
        id="weekly_reset"
    )

    def delete_expired_logs_with_context():
        print("[SCHEDULER] delete_expired_logs dijalankan")
        with app.app_context():
            delete_expired_logs()

    scheduler.add_job(
        func=delete_expired_logs_with_context,
        trigger="interval",
        days=1,  # Bisa dissesuaikan dengan kebutuhan, kapan pengeksekusian nya 
        id="daily_delete_expired_logs"
    )

    if os.environ.get("FLASK_RUN_FROM_CLI") != "true":
        try:
            scheduler.start()
        except Exception:
            pass
    # for rule in app.url_map.iter_rules():
    #         print(f"[ROUTE] {rule.methods} => {rule}")
    return app
