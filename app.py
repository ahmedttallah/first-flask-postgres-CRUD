from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kratos19010@localhost:5432/tracker'
db = SQLAlchemy(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f"Event: {self.description}"

    def __init__(self, description):
        self.description = description


def format_event(event):
    return {
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }


@app.route("/")
def index():
    return "Hello World from HomePage"

# Create an Events


@app.route("/events", methods=['POST'])
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# Get All Events


@app.route("/events", methods=['GET'])
def all_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

# Get single event or delete it


@app.route("/events/<id>", methods=['GET', 'DELETE'])
def get_or_delete_event(id):
    if (request.method == 'GET'):
        event = Event.query.filter_by(id=id).one()
        formatted_event = format_event(event)
        return {"event": formatted_event}
    elif (request.method == 'DELETE'):
        event = Event.query.filter_by(id=id).one()
        db.session.delete(event)
        db.session.commit()
        return f'Event with (id: {id}) deleted'

# Update an event


@app.route("/events/<id>", methods=['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description=description, created_at=datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}


if __name__ == '__main__':
    app.run()
