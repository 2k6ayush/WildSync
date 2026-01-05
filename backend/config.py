import os


_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_DEFAULT_SQLITE_PATH = os.path.join(_ROOT_DIR, "instance", "wildsync.db")
_DEFAULT_DB = f"sqlite:///{_DEFAULT_SQLITE_PATH}"


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-this")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _DEFAULT_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(_ROOT_DIR, "uploads"))
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    SECURITY_EMAIL_SENDER = os.getenv("SECURITY_EMAIL_SENDER", "noreply@wildsync.ai")

