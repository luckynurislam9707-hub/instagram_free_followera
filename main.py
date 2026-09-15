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


@app.route("/", methods=["GET"])
def home():
    return render_template("fronted.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    # Get visitor IP from Render's forwarded header
    forwarded = request.headers.get("X-Forwarded-For")
    print("X-Forwarded-For:", forwarded, flush=True)
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.remote_addr

    print("Visitor IP:", ip, flush=True)

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
            "ip_address": ip
        }).execute()

        return jsonify({
            "message": "Saved successfully"
        }), 200

    except Exception as error:
        print("SUPABASE ERROR:", error, flush=True)

        return jsonify({
            "error": "Could not save data"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
