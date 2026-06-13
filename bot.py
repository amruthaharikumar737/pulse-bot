# Pulse - Daily Summary Bot
import requests
from datetime import date


def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""

    url = f"https://wttr.in/{city}?format=3"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()

    except Exception as e:
        return f"Weather unavailable ({e})"


def get_quote():
    """Fetch a random motivational quote."""

    url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        quote = data[0]["q"]
        author = data[0]["a"]

        return f"{quote} — {author}"

    except Exception as e:
        return f"Quote unavailable ({e})"


def get_fact():
    """Fetch a random useless fact."""

    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        return data["text"]

    except Exception as e:
        return f"Fact unavailable ({e})"


def build_summary():
    """Assemble the full daily summary."""

    today = date.today().strftime("%d %b %Y")

    weather = get_weather()
    quote = get_quote()
    fact = get_fact()

    summary = f"""
----------------------------------------
PULSE - DAILY SUMMARY
{today}
----------------------------------------

WEATHER
{weather}

TODAY'S QUOTE
{quote}

RANDOM FACT
{fact}

----------------------------------------
"""

    return summary


def run():
    """Main entry point."""

    summary = build_summary()

    print(summary)

    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("Pulse ran successfully.")


if __name__ == "__main__":
    run()
import smtplib
import os
from email.mime.text import MIMEText

def send_email(summary_text):

    sender = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("EMAIL_RECEIVER")

    msg = MIMEText(summary_text)
    msg["Subject"] = "Pulse Daily Summary"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    print("Email sent.")
    import requests
import os

def get_weather():
    api_key = os.environ.get("WEATHER_API_KEY")
    city = "Kochi"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"{city}: {temp}°C, {desc}"

def build_summary():
    weather = get_weather()

    summary = f"""
📊 Pulse Daily Summary

🌦️ Weather:
{weather}
"""

    return summary

summary = build_summary()
send_email(summary)