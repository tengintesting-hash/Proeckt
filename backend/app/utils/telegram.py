import hashlib
import hmac
import urllib.parse
from app.core.config import settings


def validate_init_data(init_data: str) -> dict:
    parsed = dict(urllib.parse.parse_qsl(init_data, strict_parsing=True))
    hash_value = parsed.pop("hash", None)
    if not hash_value:
        raise ValueError("Missing hash")
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(parsed.items())])
    secret_key = hashlib.sha256(settings.telegram_webapp_secret.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_hash, hash_value):
        raise ValueError("Invalid hash")
    return parsed
