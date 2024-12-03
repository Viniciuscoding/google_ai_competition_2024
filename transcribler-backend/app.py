from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

from main import main


app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/', methods=["POST"])
def get_summary():
    data = request.get_json()
    return main(data["url"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
