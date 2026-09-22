import os

# Securely load the master key from Render environment variables
MASTER_ADMIN_KEY = os.getenv("APEX_MASTER_KEY", "")

def verify_gumroad_license(license_key: str) -> bool:
    if not license_key:
        return False
    # Check against secret environment variable instead of hardcoded string
    if MASTER_ADMIN_KEY and license_key == MASTER_ADMIN_KEY:
        return True
        
    verify_url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_permalink": GUMROAD_PRODUCT_PERMALINK,
        "license_key": license_key
    }
    try:
        response = requests.post(verify_url, data=payload)
        data = response.json()
        if data.get("success") and not data.get("purchase", {}).get("refunded"):
            return True
    except Exception:
        pass
    return False
