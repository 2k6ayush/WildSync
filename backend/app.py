import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import logging


load_dotenv()

from .config import Config
from .extensions import db, migrate, login_manager, mail


logger = logging.getLogger(__name__)


def register_blueprints(app: Flask):
    # Import and register blueprints individually, skipping optional ones if deps missing
    try:
        from .routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
    except Exception as e:
        logger.warning("Skipping auth blueprint: %s", e)

    try:
        from .routes.uploads import uploads_bp
        app.register_blueprint(uploads_bp, url_prefix="/api/uploads")
    except Exception as e:
        logger.warning("Skipping uploads blueprint (optional deps likely missing): %s", e)

    try:
        from .routes.analysis import analysis_bp
        app.register_blueprint(analysis_bp, url_prefix="/api/analysis")
    except Exception as e:
        logger.warning("Skipping analysis blueprint: %s", e)

    try:
        from .routes.maps import maps_bp
        app.register_blueprint(maps_bp, url_prefix="/api/maps")
    except Exception as e:
        logger.warning("Skipping maps blueprint: %s", e)

    try:
        from .routes.chatbot import chatbot_bp
        app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
    except Exception as e:
        logger.warning("Skipping chatbot blueprint: %s", e)

    try:
        from .routes.community import community_bp
        app.register_blueprint(community_bp, url_prefix="/api/community")
    except Exception as e:
        logger.warning("Skipping community blueprint: %s", e)

    try:
        from .routes.profile import profile_bp
        app.register_blueprint(profile_bp, url_prefix="/api/profile")
    except Exception as e:
        logger.warning("Skipping profile blueprint: %s", e)


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:///"):
        db_path = db_uri.replace("sqlite:///", "", 1)
        if db_path:
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

    # Extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    register_blueprints(app)

    # Auto-create DB tables for local sqlite, or when explicitly enabled.
    auto_create_env = os.getenv("DB_AUTOCREATE")
    auto_create = False
    if auto_create_env is None:
        auto_create = db_uri.startswith("sqlite:///")
    else:
        auto_create = auto_create_env.lower() in ("1", "true", "yes", "y")

    if auto_create:
        try:
            # Ensure models are imported so SQLAlchemy knows all tables
            from . import models  # noqa: F401
            with app.app_context():
                db.create_all()
            logger.info("DB_AUTOCREATE: created all tables (or already existed)")
        except Exception as e:
            logger.warning("DB_AUTOCREATE failed: %s", e)

    if os.getenv("DB_SEED", "false").lower() in ("1", "true", "yes", "y"):
        try:
            from .cli import seed  # type: ignore
            with app.app_context():
                seed()
            logger.info("DB_SEED: seeding completed or already present")
        except Exception as e:
            logger.warning("DB_SEED failed: %s", e)

    # CLI commands
    try:
        from .cli import register_cli  # noqa: WPS433
        register_cli(app)
    except Exception:
        # CLI registration is optional for runtime
        pass

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}

    return app
