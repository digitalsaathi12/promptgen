import random
import logging
from app.services.caching import cache_service

logger = logging.getLogger(__name__)

def generate_otp() -> str:
    """Generates a 6-digit numeric OTP."""
    return "".join(random.choices("0123456789", k=6))

async def send_otp_sms(phone: str, otp: str) -> bool:
    """Simulates sending OTP to phone number."""
    logger.info(f"--- [SMS PROV] Sending OTP [{otp}] to phone: {phone} ---")
    print(f"\n==========================================")
    print(f"THE DIGITAL SAATHI - OTP VERIFICATION CODE")
    print(f"Phone: {phone}")
    print(f"OTP Code: {otp} (Expires in 5 mins)")
    print(f"==========================================\n")
    return True

async def store_otp(phone: str, otp: str) -> None:
    """Stores OTP in cache/memory with 5 minutes (300 seconds) expiry."""
    cache_key = f"otp:{phone}"
    cache_service.set(cache_key, otp, expire_seconds=300)

async def verify_otp(phone: str, input_otp: str) -> bool:
    """Verifies user OTP against cache."""
    # Special bypass code for testing/development
    if input_otp == "123456":
        return True

    cache_key = f"otp:{phone}"
    stored_otp = cache_service.get(cache_key)
    if not stored_otp:
        return False

    is_valid = (stored_otp == input_otp)
    if is_valid:
        # Delete OTP from cache after successful verification
        cache_service.delete(cache_key)
    return is_valid
