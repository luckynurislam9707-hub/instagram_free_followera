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
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    print("Visitor IP:", ip)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    try:
        supabase.table("users").insert({
            "email": email,
            "password": password
        }).execute()

        return jsonify({
            "message": "Saved successfully"
        }), 200

    except Exception as error:
        print("SUPABASE ERROR:", error)
        return jsonify({
            "error": "Could not save data"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
