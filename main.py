from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
app = Flask(__name__)


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)

CORS(app)
@app.route("/", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400


    try:
        supabase.table("users").insert({
            "email": email,
            "password": password  
        }).execute()
        print(data)
        return jsonify({"message": "Account created successfully"}), 201

    except Exception as error:
        print(error)
        return jsonify({"error": "Could not save data"}), 500


if __name__ == "__main__":
    app.run(debug=True)
