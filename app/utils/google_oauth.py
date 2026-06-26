import logging
from typing import Optional, Dict, Any
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings

logger = logging.getLogger(__name__)

def verify_google_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifies a Google ID token.
    
    Returns:
        dict: User info from Google payload (email, name, picture, etc.) or None if invalid.
    """
    # Mock token validation for testing or development
    if token.startswith("mock-") or settings.GOOGLE_CLIENT_ID == "mock-google-client-id":
        logger.info("Verifying mock Google token.")
        # Simulated payload
        email = f"{token.replace('mock-', '')}@gmail.com"
        name = token.replace("mock-", "").capitalize() or "Google User"
        return {
            "sub": f"google_{token}",
            "email": email,
            "email_verified": True,
            "name": name,
            "picture": "https://lh3.googleusercontent.com/a/mock-avatar.png"
        }

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        return id_info
    except Exception as e:
        logger.error(f"Google ID token verification failed: {e}")
        return None
