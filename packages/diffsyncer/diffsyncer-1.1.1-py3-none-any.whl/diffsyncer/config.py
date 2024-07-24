import os
from dotenv import load_dotenv

load_dotenv()

REPO_DIR = os.path.join(os.getcwd(), os.getenv("REPO_DIR", "repo"))

# output directory for qr codes
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(os.getcwd(), "output"))

# diff data directory
DIFF_DIR = os.getenv("DIFF_DIR", os.path.join(OUTPUT_DIR, "diff"))

# upload directory for files
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.getcwd(), "upload"))

ASE_KEY_FILE = os.getenv("ASE_KEY_FILE", os.path.join(os.getcwd(), "aes_key.bin"))

COMPRESS_METHOD = os.getenv("COMPRESS_METHOD", "zstd")

CHUNK_SIZE = os.getenv("CHUNK_SIZE", 800)

# admin username and password, default admin/admin
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD", "$2b$12$f9l0H6Atq0cZUo5ceuLvx.ZoD0yxYguaI9u7JVJ8Mk9r8STcAGXXO"
)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "2e5ede831c9ab79ef213d88035bb28f4a69cbf8b5e9c9c1e47c6bf61372bbc38"
ALGORITHM = "HS256"
# access token expire time in seconds, default 2 hours
ACCESS_TOKEN_EXPIRE_SECONDS = 7200
