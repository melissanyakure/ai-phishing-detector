
from flask import Flask, render_template, request
import joblib
import re
import sqlite3
import ipaddress
from urllib.parse import urlparse
from datetime import datetime

app = Flask(__name__)

# Load the trained AI model
model = joblib.load("model/phishing_model.pkl")


# Create database and history table
def create_database():
    connection = sqlite3.connect("phishing_history.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            date_checked TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Save email analysis to database
def save_history(email_text, prediction, confidence):
    connection = sqlite3.connect("phishing_history.db")

    connection.execute("""
        INSERT INTO history
        (email_text, prediction, confidence, date_checked)
        VALUES (?, ?, ?, ?)
    """, (
        email_text,
        prediction,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()


# Retrieve email detection history
def get_history():
    connection = sqlite3.connect("phishing_history.db")
    connection.row_factory = sqlite3.Row

    records = connection.execute(
        "SELECT * FROM history ORDER BY id DESC"
    ).fetchall()

    connection.close()
    return records


# Calculate dashboard statistics
def get_dashboard_stats():
    connection = sqlite3.connect("phishing_history.db")

    total = connection.execute(
        "SELECT COUNT(*) FROM history"
    ).fetchone()[0]

    phishing = connection.execute(
        "SELECT COUNT(*) FROM history WHERE prediction = 'Phishing'"
    ).fetchone()[0]

    legitimate = connection.execute(
        "SELECT COUNT(*) FROM history WHERE prediction = 'Legitimate'"
    ).fetchone()[0]

    phishing_percentage = (
        round((phishing / total) * 100, 2)
        if total > 0 else 0
    )

    connection.close()

    return {
        "total": total,
        "phishing": phishing,
        "legitimate": legitimate,
        "phishing_percentage": phishing_percentage
    }


# Extract URLs from emails
def extract_urls(email_text):
    pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(pattern, email_text, re.IGNORECASE)


# Check URLs for common warning signs
def check_url(url):
    warnings = []

    if url.lower().startswith("www."):
        url = "http://" + url

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or ""

    if parsed_url.scheme == "http":
        warnings.append("Uses HTTP instead of HTTPS")

    if hostname:
        try:
            ipaddress.ip_address(hostname)
            warnings.append("Uses an IP address instead of a domain name")
        except ValueError:
            pass

    suspicious_words = [
        "login", "verify", "account", "secure",
        "update", "password", "bank", "confirm"
    ]

    for word in suspicious_words:
        if word in hostname.lower():
            warnings.append("Contains suspicious word: " + word)

    if "@" in url:
        warnings.append("Contains an @ symbol")

    return warnings


# Main website
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    email_text = ""
    url_results = []

    if request.method == "POST":
        email_text = request.form.get("email", "").strip()

        if email_text:
            prediction = model.predict([email_text])[0]
            probabilities = model.predict_proba([email_text])[0]

            confidence = round(max(probabilities) * 100, 2)

            if prediction == 1:
                prediction_label = "Phishing"
                result = {
                    "message": "WARNING: This email is likely PHISHING!",
                    "type": "phishing",
                    "confidence": confidence
                }
            else:
                prediction_label = "Legitimate"
                result = {
                    "message": "This email is likely LEGITIMATE.",
                    "type": "legitimate",
                    "confidence": confidence
                }

            # Save analysis to database
            save_history(email_text, prediction_label, confidence)

            # Analyse URLs found in email
            urls = extract_urls(email_text)

            for url in urls:
                url_results.append({
                    "url": url,
                    "warnings": check_url(url)
                })

    # Retrieve history and dashboard statistics
    history = get_history()
    stats = get_dashboard_stats()

    return render_template(
        "index.html",
        result=result,
        email_text=email_text,
        url_results=url_results,
        history=history,
        stats=stats
    )


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
