import os

from urllib.parse import quote_plus

from dotenv import load_dotenv


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# FLASK CONFIG
# =====================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-secret-key"
)

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() in (
    "true",
    "1",
    "yes"
)


# =====================================================
# MYSQL DATABASE CONFIG
# =====================================================

MYSQL_USER = os.getenv(
    "MYSQL_USER",
    "root"
)

MYSQL_PASSWORD = os.getenv(
    "MYSQL_PASSWORD",
    ""
)

MYSQL_HOST = os.getenv(
    "MYSQL_HOST",
    "localhost"
)

MYSQL_PORT = os.getenv(
    "MYSQL_PORT",
    "3306"
)

MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "campus_at_desk"
)


# =====================================================
# DATABASE URI
# =====================================================

DATABASE_URI = (

    os.getenv("DATABASE_URL")

    or

    os.getenv("DATABASE_URI")

    or

    (
        f"mysql+pymysql://"
        f"{quote_plus(MYSQL_USER)}:"
        f"{quote_plus(MYSQL_PASSWORD)}"
        f"@{MYSQL_HOST}:"
        f"{MYSQL_PORT}/"
        f"{MYSQL_DATABASE}"
    )
)


# =====================================================
# FILE UPLOADS
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads",
    "resumes"
)

ALLOWED_RESUME_EXTENSIONS = {
    "pdf",
    "doc",
    "docx"
}