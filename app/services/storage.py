import os
import uuid
import logging
from typing import Union
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket_name = settings.SUPABASE_BUCKET
        self.client = None

        if self.supabase_url and self.supabase_key:
            try:
                # Proactively load supabase client
                from supabase import create_client
                self.client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase storage client initialized.")
            except Exception as e:
                logger.warning(f"Could not initialize Supabase client: {e}. Local fallback will be used.")

    async def upload_image(self, file_bytes: bytes, filename: str = None) -> str:
        """Uploads image bytes and returns the accessible public URL."""
        if not filename:
            filename = f"{uuid.uuid4()}.png"

        # If Supabase is configured, upload to bucket
        if self.client:
            try:
                # Supabase storage upload
                storage = self.client.storage.from_(self.bucket_name)
                # Upload files as bytes
                response = storage.upload(
                    path=filename,
                    file=file_bytes,
                    file_options={"content-type": "image/png"}
                )
                # Get public URL
                public_url = storage.get_public_url(filename)
                logger.info(f"Uploaded to Supabase: {public_url}")
                return public_url
            except Exception as e:
                logger.error(f"Supabase upload failed: {e}. Falling back to local storage.")

        # Fallback: Save locally inside standard public uploads folder
        static_dir = os.path.join(os.getcwd(), "static", "uploads")
        os.makedirs(static_dir, exist_ok=True)
        file_path = os.path.join(static_dir, filename)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        # Return a simulated or local development URL
        logger.info(f"Saved locally: static/uploads/{filename}")
        return f"/static/uploads/{filename}"

storage_service = StorageService()
