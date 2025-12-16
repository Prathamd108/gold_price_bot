import os  # <--- Added this to talk to the Cloud
import yfinance as yf
import requests
import datetime

# --- CONFIGURATION (SECURE MODE) ---
# We do NOT paste keys here. We ask GitHub for them.
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Safety Check: Stop if keys are missing
if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("❌ FATAL ERROR: Secrets not found. Did you add them in GitHub Settings?")
# -----------------------------------

def send_telegram_alert(message):
    """Sends the message to your Telegram App"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
        print("📨 Message sent to Telegram!")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

def run_agent():
    print("\n🚀 AGENT ACTIVE: Checking Markets...")
    
    # 1. FETCH DATA
    try:
        gold_etf = yf.Ticker("GOLDBEES.NS")
        data = gold_etf.history(period="1d")
        
        if data.empty:
            print("❌ Market Closed/No Data")
            return

        unit_price = data['Close'].iloc[-1]
        price_10g = unit_price * 1000 
        
        # 2. DECISION LOGIC
        buy_threshold = 110000 
        date_now = datetime.datetime.now().strftime('%d-%b-%Y')
        
        if price_10g < buy_threshold:
            status = "🟢 *BUY ALERT*"
            advice = "Gold is trading below ₹1.10L. Good time to accumulate."
        else:
            status = "🔴 *WAIT ALERT*"
            advice = "Price is high. Wait for a dip."

        msg = f"""
{status}
📅 {date_now}

💰 *Pune Gold Rate (Est. 10g):* ₹{price_10g:,.0f}
📉 *ETF Unit:* ₹{unit_price:.2f}

💡 *Advice:* {advice}
        """
        
        # 3. DELIVERY
        print(msg) 
        send_telegram_alert(msg) 
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_agent()
