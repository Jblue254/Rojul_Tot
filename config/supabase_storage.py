
import os
import uuid
from pathlib import Path

from django.conf import settings
from supabase import create_client


BUCKETS = {
    "machinery": "machinery-images",
    "projects": "project-images",
    "previews": "drawing-previews",
    "drawings": "drawing-files",
}


def get_supabase_client():
    url = getattr(settings, "SUPABASE_URL", "")
    key = getattr(settings, "SUPABASE_SERVICE_ROLE_KEY", "")

    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured."
        )

    return create_client(url, key)


def upload_file(file_obj, bucket_name, folder=""):
    """Upload a Django uploaded file and return its storage path."""
    client = get_supabase_client()

    original_name = Path(file_obj.name).name
    extension = Path(original_name).suffix.lower()
    storage_name = f"{uuid.uuid4().hex}{extension}"

    folder = folder.strip("/")
    storage_path = (
        f"{folder}/{storage_name}" if folder else storage_name
    )

    content_type = (
        getattr(file_obj, "content_type", None)
        or "application/octet-stream"
    )

    file_obj.seek(0)

    client.storage.from_(bucket_name).upload(
        path=storage_path,
        file=file_obj.read(),
        file_options={
            "content-type": content_type,
            "upsert": "false",
        },
    )

    return storage_path


def public_file_url(bucket_name, storage_path):
    if not storage_path:
        return None

    client = get_supabase_client()

    return client.storage.from_(bucket_name).get_public_url(
        storage_path
    )


def download_private_file(bucket_name, storage_path):
    """Download a private object on the server after authorization."""
    if not storage_path:
        return None

    client = get_supabase_client()

    return client.storage.from_(bucket_name).download(storage_path)
