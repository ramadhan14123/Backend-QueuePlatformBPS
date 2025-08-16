from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/*": {"origins": ["https://bukutamu.pahlawan140.com"]}}, supports_credentials=True)

if __name__ == "__main__":
    app.run(debug=True)
