from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/*": {"origins": ["https://bukutamu.pahlawan140.com"]}})

if __name__ == "__main__":
    app.run(debug=True) #development
