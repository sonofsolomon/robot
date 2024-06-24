from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Keystroke Data Model
class KeystrokeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keystrokes = db.Column(db.Text)  # This will store a JSON string

    def set_keystrokes(self, keystrokes):
        self.keystrokes = json.dumps(keystrokes)

    def get_keystrokes(self):
        return json.loads(self.keystrokes)

class MouseMoveData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movements = db.Column(db.Text)  # Stores JSON string of mouse movements

    def set_movements(self, movements):
        self.movements = json.dumps(movements)

    def get_movements(self):
        return json.loads(self.movements)

class MouseClickData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    clicks = db.Column(db.Text)  # Stores JSON string of mouse clicks

    def set_clicks(self, clicks):
        self.clicks = json.dumps(clicks)

    def get_clicks(self):
        return json.loads(self.clicks)

# Fingerprint Data Model including Canvas Fingerprint
class FingerprintData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_agent = db.Column(db.String(256))
    screen_resolution = db.Column(db.String(50))
    language = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    ip_address = db.Column(db.String(50))  # Storing IP address
    canvas_fingerprint = db.Column(db.Text)  # New column for storing canvas fingerprint
    fonts = db.Column(db.Text)  # New field for storing detected fonts
    device_memory = db.Column(db.String(50))  # Client hint: device memory
    hardware_concurrency = db.Column(db.String(50))  # Client hint: hardware concurrency
    viewport_width = db.Column(db.String(50))  # Client hint: viewport width

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    # Check if a user with the provided email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        # If a user with this email already exists, return an error message
        return jsonify({"message": "Email already in use."}), 400

    # Create a new user since the email is not in use
    user = User(
        full_name=data['fullName'],
        email=data['email']
    )
    user.set_password(data['password'])  # Hash the password before storing it
    db.session.add(user)
    db.session.commit()  # Commit the new user to the database

    # Collect and store additional fingerprinting data
    fingerprint = data.get('fingerprintData', {})
    db.session.add(FingerprintData(
        user_id=user.id,
        user_agent=fingerprint.get('userAgent'),
        screen_resolution=fingerprint.get('screenResolution'),
        language=fingerprint.get('language'),
        platform=fingerprint.get('platform'),
        ip_address=request.remote_addr,  # Capture the user's IP address from the request
        fonts=json.dumps(data.get('fingerprintData', {}).get('fonts', [])),  # Store fonts as JSON string
        device_memory=data.get('fingerprintData', {}).get('clientHints', {}).get('deviceMemory', 'unknown'),
        hardware_concurrency=data.get('fingerprintData', {}).get('clientHints', {}).get('hardwareConcurrency', 'unknown'),
        viewport_width=data.get('fingerprintData', {}).get('clientHints', {}).get('viewportWidth', 'unknown'),
        canvas_fingerprint=fingerprint.get('canvasFingerprint')  # Store the canvas fingerprint
    ))

        # Process and store keystroke data
    # After creating a new user
    keystroke_data = data.get('keystrokeData', [])
    if keystroke_data:
        db.session.add(KeystrokeData(user_id=user.id, keystrokes=json.dumps(keystroke_data)))
    # Process and store mouse move data
    mouse_move_data = data.get('mouseMoveData', [])
    if mouse_move_data:
        db.session.add(MouseMoveData(user_id=user.id, movements=json.dumps(mouse_move_data)))

    # Process and store mouse click data
    mouse_click_data = data.get('mouseClickData', [])
    if mouse_click_data:
        db.session.add(MouseClickData(user_id=user.id, clicks=json.dumps(mouse_click_data)))

    # Commit the session to save the fingerprint data
    db.session.commit()

    # Return a success message indicating the user was registered
    return jsonify({"message": "User registered successfully!"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()  # Normalize email by trimming whitespace and converting to lowercase
    password = data.get('password', '')
    
    print(f"Normalized Email: {email}")  # Debug print to check the normalized email

    user = User.query.filter_by(email=email).first()

    if user is None:
        print("No user found with the provided email.")  # Debugging message
        return jsonify({"message": "Invalid email or password"}), 401
    print("Here")
    # Check if the "robotCheck" field matches the expected string
    if not data.get('robotCheck') or data.get('robotCheck').lower() != "i am not a robot":
        print("robot check passwed")
        return jsonify({"message": "Please confirm you are not a robot."}), 400

    if user.check_password(password):
        print("check password")
        fingerprint = data.get('fingerprintData', {})
        db.session.add(FingerprintData(
            user_id=user.id,
            user_agent=fingerprint.get('userAgent'),
            screen_resolution=fingerprint.get('screenResolution'),
            language=fingerprint.get('language'),
            platform=fingerprint.get('platform'),
            ip_address=request.remote_addr,
            fonts=json.dumps(data.get('fingerprintData', {}).get('fonts', [])),  # Store fonts as JSON string
            device_memory=data.get('fingerprintData', {}).get('clientHints', {}).get('deviceMemory', 'unknown'),
            hardware_concurrency=data.get('fingerprintData', {}).get('clientHints', {}).get('hardwareConcurrency', 'unknown'),
            viewport_width=data.get('fingerprintData', {}).get('clientHints', {}).get('viewportWidth', 'unknown'),
            canvas_fingerprint=fingerprint.get('canvasFingerprint')
        ))
        db.session.commit()
        print("committed")
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid email or password"}), 401



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)