from google.cloud import storage
import os
from dotenv import load_dotenv


load_dotenv()

# Fungsi untuk menginisialisasi klien Google Cloud Storage
def get_storage_client():
    # Ambil kredensial dari variabel lingkungan
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    # Mengecek kredensial terisi dengan benar
    if not cred_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    # Inisialisasi klien Google Cloud Storage dengan kredensial service account json
    client = storage.Client.from_service_account_json(cred_path)
    return client

# Fungsi untuk mengambil bucket berdasarkan nama yang disimpan di file .env
def get_bucket_from_env():
    # Ambil nama bucket dari file .env
    bucket_name = os.getenv("BUCKET_NAME")

    # Mengecek nama bucket terisi dengan benar
    if not bucket_name:
        raise ValueError("BUCKET_NAME environment variable is not set.")

    # Dapatkan klien dan bucket
    client = get_storage_client()
    bucket = client.get_bucket(bucket_name)
    return bucket

# Fungsi untuk mendapatkan semua bucket yang ada di proyek Google Cloud
def list_buckets():
    client = get_storage_client()
    buckets = client.list_buckets()
    
    bucket_names = []
    for bucket in buckets:
        bucket_names.append(bucket.name)
    
    return bucket_names

# Fungsi untuk mendapatkan bucket pertama dari daftar
def get_first_bucket():
    bucket_names = list_buckets()
    if bucket_names:
        return get_bucket_from_env()  # Ganti dengan bucket yang dipilih dari .env
    else:
        raise ValueError("No buckets found in the project.")
