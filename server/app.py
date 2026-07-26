from flask import Flask, jsonify, request


try:
    from flask_migrate import Migrate
except ModuleNotFoundError:
    Migrate = None

from server.models import db, Event, Session, Speaker, Bio


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

if Migrate:
    migrate = Migrate(app, db)


@app.route("/")
def home():
    return {
        "message": "EventWise API"
    }, 200


# GET all events
@app.route("/events")
def get_events():

    events = Event.query.all()

    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]), 200


# POST event
@app.route("/events", methods=["POST"])
def create_event():

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "title is required"
        }), 400

    event = Event(
        name=data["title"],
        location=data.get("location", "")
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({
        "id": event.id,
        "title": event.name
    }), 201


# Event sessions
@app.route("/events/<int:id>/sessions")
def get_event_sessions(id):

    event = Event.query.get(id)

    if not event:
        return {
            "error": "Event not found"
        }, 404

    return jsonify([
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
            if session.start_time else None
        }
        for session in event.sessions
    ]), 200


# Speakers
@app.route("/speakers")
def get_speakers():

    speakers = Speaker.query.all()

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]), 200


# Speaker details
@app.route("/speakers/<int:id>")
def get_speaker(id):

    speaker = Speaker.query.get(id)

    if not speaker:
        return {
            "error": "Speaker not found"
        }, 404

    return {
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text
        if speaker.bio else "No bio available"
    }, 200


# Session speakers
@app.route("/sessions/<int:id>/speakers")
def get_session_speakers(id):

    session = Session.query.get(id)

    if not session:
        return {
            "error": "Session not found"
        }, 404

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": speaker.bio.bio_text
            if speaker.bio else "No bio available"
        }
        for speaker in session.speakers
    ]), 200


if __name__ == "__main__":
    app.run(port=5555)