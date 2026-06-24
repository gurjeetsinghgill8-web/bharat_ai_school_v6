"""
Bharat AI School V6 — Payment System
₹20/month subscription via UPI (Phase 1) and Razorpay (Phase 2).
"""
from datetime import datetime, timedelta
from db import operations as db_ops

# ── UPI Details ──
UPI_ID = "gurjas@upi"          # ← Change to your actual UPI ID
UPI_NAME = "Dr. Gurjas Singh"  # ← Change to your name
UPI_QR_PATH = ""               # ← Add path to QR code image if available
SUBSCRIPTION_PRICE = 20.0
SUBSCRIPTION_DAYS = 30

# ── Admin UPI verification ──
PENDING_TXNS = {}  # Temporary in-memory store (replace with DB in prod)


def get_upi_payment_details():
    """Return UPI details for the user to make payment."""
    return {
        "upi_id": UPI_ID,
        "name": UPI_NAME,
        "amount": SUBSCRIPTION_PRICE,
        "description": f"Bharat AI School - {SUBSCRIPTION_DAYS} days subscription",
        "qr_path": UPI_QR_PATH,
    }

def generate_upi_url(amount: float = SUBSCRIPTION_PRICE, note: str = "Bharat AI School") -> str:
    """Generate an intent-based UPI URL for auto-fill."""
    from urllib.parse import quote
    note_encoded = quote(note[:30])  # UPI limits note length
    return f"upi://pay?pa={UPI_ID}&pn={quote(UPI_NAME)}&am={amount:.2f}&cu=INR&tn={note_encoded}"

def record_payment(username: str, amount: float, txn_id: str, method: str = "UPI"):
    """Record a payment and activate subscription."""
    db_ops.create_subscription(username, amount, method, txn_id)
    return True

def check_subscription_status(username: str) -> dict:
    """Check if user has an active subscription or pending verification. Returns status info."""
    active = db_ops.has_active_subscription(username)
    sub = db_ops.get_active_subscription(username)
    
    if active and sub:
        end = sub.get("end_date", "")
        days_left = 0
        if end:
            try:
                end_dt = datetime.fromisoformat(end)
                days_left = max(0, (end_dt - datetime.now()).days)
            except:
                pass
        
        return {
            "active": True,
            "pending": False,
            "plan": sub.get("plan_type", "monthly"),
            "end_date": end,
            "days_left": days_left,
            "amount_paid": sub.get("amount_paid", 20),
        }
    
    # Check for pending subscriptions
    pending_sub = db_ops.get_pending_subscription(username)
    if pending_sub:
        return {
            "active": False,
            "pending": True,
            "plan": pending_sub.get("plan_type", "monthly"),
            "end_date": None,
            "days_left": 0,
            "amount_paid": pending_sub.get("amount_paid", 20),
            "transaction_id": pending_sub.get("transaction_id", ""),
        }
    
    return {"active": False, "pending": False, "plan": None, "end_date": None, "days_left": 0, "amount_paid": 0}

def get_subscription_required_message() -> str:
    """Return message to show when subscription is needed."""
    return f"""
🔒 **यह feature सिर्फ सब्सक्राइबर्स के लिए है।**

👉 **₹{int(SUBSCRIPTION_PRICE)}/माह** — पूरा curriculum, PDF downloads, streaks और AI टीचर से बातचीत।

**UPI ID:** `{UPI_ID}`
**Amount:** ₹{int(SUBSCRIPTION_PRICE)}

Payment करने के बाद transaction ID डालें और admin verify करेगा।
"""
