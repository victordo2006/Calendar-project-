from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import calendar
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from React

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedule.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

    
# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task %r>' % self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.isoformat(),
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "location": self.location,
            "description": self.description,
            "completed": self.completed
        }
 
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

# API Routes
@app.route("/api/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        date = request.args.get('date')
        if date:
            # Convert string date to datetime object
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            tasks = Task.query.filter_by(date=date_obj).all()
        else:
            tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    elif request.method == "POST":
        data = request.json
        new_task = Task(
            title=data["title"],
            date=datetime.strptime(data["date"], '%Y-%m-%d').date(),
            start=datetime.strptime(data["start"], '%H:%M').time(),
            end=datetime.strptime(data["end"], '%H:%M').time(),
            location=data.get("location", ""),
            description=data.get("description", "")
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict())

@app.route("/api/calendar", methods=["GET"])
def get_calendar():
    now = datetime.now()
    year = int(request.args.get('year', now.year))
    month = int(request.args.get('month', now.month))

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    return jsonify({"calendar": cal, "month_name": month_name, "year": year, "month": month})

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password']  # Note: Passwords should be hashed in a real application
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict())



if __name__ == "__main__":
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        print("Database tables recreated successfully!")
    app.run(debug=True)
