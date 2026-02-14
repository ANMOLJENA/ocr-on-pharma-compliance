from flask import Flask, jsonify
from flask_cors import CORS
import os
import platform

# Set up Poppler path for PDF processing on Windows
if platform.system() == 'Windows':
    poppler_paths = [
        r'C:\Users\KIIT0001\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin',
        r'C:\Program Files\poppler\Library\bin',
        r'C:\Program Files (x86)\poppler\Library\bin'
    ]
    for path in poppler_paths:
        if os.path.exists(path):
            os.environ['POPPLER_PATH'] = path
            break

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr_compliance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'tiff'}

# Initialize database
from database import db
db.init_app(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import and register blueprints
from routes import ocr_routes, analytics_routes
app.register_blueprint(ocr_routes.bp)
app.register_blueprint(analytics_routes.bp)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'OCR Compliance API is running'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
