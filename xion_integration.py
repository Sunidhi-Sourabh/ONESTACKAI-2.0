# xion_integration.py

def verify_user_xion(user_id):
    """
    Simulates XION walletless verification.
    Always returns True in mock mode.
    """
    # For demo purposes, all users are verified
    return True

def get_zktls_proof(user_id):
    """
    Returns a mock zkTLS proof payload with fallback trigger.
    """
    verified = verify_user_xion(user_id)
    return {
        "user_id": user_id,
        "proof": "zkTLS_stub_1234567890",
        "verified": verified,
        "fallback_triggered": not verified
    }
