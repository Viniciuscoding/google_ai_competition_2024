from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS  # Import CORS

from main import main
from pytube import YouTube

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/', methods=["POST"])
def get_summary():
    data = request.get_json()
    file_path = main(data["url"])
    
    # Ensure the file path is correctly formatted
    file_path = file_path.strip('"')
    
    blob = send_file(file_path, as_attachment=True)
    response = blob
    print(f"response type: {type(response)}")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
