from flask import Flask
from flask_cors import CORS  # Import CORS

from main import main


app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/')
def get_summary():
    return main()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
