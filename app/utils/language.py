import re

# Devanagari range is U+0900 to U+097F
HINDI_CHAR_REGEX = re.compile(r"[\u0900-\u097f]+")

def detect_hindi(text: str) -> bool:
    """Detects if a given string contains Hindi (Devanagari) characters."""
    if not text:
        return False
    return bool(HINDI_CHAR_REGEX.search(text))

# Simple localized response messages
MESSAGES = {
    "en": {
        "welcome": "Welcome to The Digital Saathi",
        "auth_success": "Authentication successful",
        "invalid_credentials": "Invalid email/phone or password",
        "otp_sent": "OTP sent successfully to your phone",
        "otp_invalid": "The OTP code provided is invalid or has expired",
        "unauthorized": "Access denied. Insufficient permissions",
    },
    "hi": {
        "welcome": "द डिजिटल साथी में आपका स्वागत है",
        "auth_success": "सत्यापन सफल रहा",
        "invalid_credentials": "अमान्य ईमेल/फ़ोन या पासवर्ड",
        "otp_sent": "ओटीपी आपके फोन पर सफलतापूर्वक भेज दिया गया है",
        "otp_invalid": "प्रदान किया गया ओटीपी कोड अमान्य है या समाप्त हो गया है",
        "unauthorized": "पहुंच अस्वीकृत। अपर्याप्त अनुमतियां",
    }
}

def get_message(key: str, lang: str = "en") -> str:
    """Retrieves standard translations by key."""
    lang = lang.lower() if lang else "en"
    if lang not in MESSAGES:
        lang = "en"
    return MESSAGES[lang].get(key, MESSAGES["en"].get(key, ""))
