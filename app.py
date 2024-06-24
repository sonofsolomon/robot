from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={r"/handle_data": {"origins": "*", "methods": ["POST"], "allow_headers": ["Content-Type", "Authorization"]}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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
    key = db.Column(db.String(50))
    timestamp = db.Column(db.Float)

# Mouse Move Data Model
class MouseMoveData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    timestamp = db.Column(db.Float)

# Mouse Click Data Model
class MouseClickData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    timestamp = db.Column(db.Float)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user = User(
        full_name=data['fullName'],
        email=data['email']
    )
    user.set_password(data['password'])
    db.session.add(user)

    # Save keystroke, mouse movement, and mouse click data
    for item in data.get('keystrokeData', []):
        db.session.add(KeystrokeData(key=item['key'], timestamp=item['timeStamp']))
    for item in data.get('mouseMoveData', []):
        db.session.add(MouseMoveData(x=item['x'], y=item['y'], timestamp=item['timeStamp']))
    for item in data.get('mouseClickData', []):
        db.session.add(MouseClickData(x=item['x'], y=item['y'], timestamp=item['timeStamp']))

    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    robotCheck = data.get('robotCheck', '').lower()
    if robotCheck != "i am not a robot":
        return jsonify({"message": "Unauthorized access. Please verify you are not a robot."}), 401

    if user and user.check_password(data['password']):
        # Save keystroke, mouse movement, and mouse click data
        for item in data.get('keystrokeData', []):
            db.session.add(KeystrokeData(key=item['key'], timestamp=item['timeStamp']))
        for item in data.get('mouseMoveData', []):
            db.session.add(MouseMoveData(x=item['x'], y=item['y'], timestamp=item['timeStamp']))
        for item in data.get('mouseClickData', []):
            db.session.add(MouseClickData(x=item['x'], y=item['y'], timestamp=item['timeStamp']))

        db.session.commit()
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
