from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# add association table

class SessionSpeaker(db.Model):
    __tablename__ = "session_speakers"

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        primary_key=True
    )

    speaker_id = db.Column(
        db.Integer,
        db.ForeignKey("speakers.id"),
        primary_key=True
    )


# set up relationships for all models
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)

    # One Event -> Many Sessions
    sessions = db.relationship(
        "Session",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer)

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False
    )

       # Belongs to Event
    event = db.relationship(
        "Event",
        back_populates="sessions"
    )

    # Many-to-Many with Speaker
    speakers = db.relationship(
        "Speaker",
        secondary="session_speakers",
        back_populates="sessions"
    )


    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True)

      # One-to-One with Bio
    bio = db.relationship(
        "Bio",
        back_populates="speaker",
        uselist=False,
        cascade="all, delete-orphan"
    )

     # Many-to-Many with Session
    sessions = db.relationship(
        "Session",
        secondary="session_speakers",
        back_populates="speakers"
    )

    def __repr__(self):
        return f'<Speaker {id}, {name}>'

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer)

    speaker_id = db.Column(
        db.Integer,
        db.ForeignKey("speakers.id"),
        unique=True,
        nullable=False
    )

    # Belongs to Speaker
    speaker = db.relationship(
        "Speaker",
        back_populates="bio"
    )

    def __repr__(self):
        return f'<Bio {id}, {bio_text}>'
