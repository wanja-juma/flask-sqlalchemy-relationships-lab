# Conference Management API

## Overview

The Conference Management API is a RESTful web application built with **Flask**, **Flask-SQLAlchemy**, and **Flask-Migrate**. It manages conferences by organizing events, sessions, speakers, and speaker biographies while demonstrating one-to-many, one-to-one, and many-to-many database relationships.

The application exposes API endpoints that allow clients to retrieve events, their sessions, speakers, speaker biographies, and session participants in JSON format.

---

## Features

* View all conference events.
* View all sessions belonging to a specific event.
* View all speakers.
* View a speaker together with their biography.
* View all speakers assigned to a session.
* JSON API responses with appropriate HTTP status codes.
* Error handling for resources that do not exist.
* Database relationships implemented using Flask-SQLAlchemy.

---

## Database Relationships

The application models the following relationships:

### One-to-Many

* An **Event** has many **Sessions**.
* A **Session** belongs to one **Event**.

### One-to-One

* A **Speaker** has one **Bio**.
* A **Bio** belongs to one **Speaker**.

### Many-to-Many

* A **Session** has many **Speakers**.
* A **Speaker** can participate in many **Sessions**.
* The relationship is implemented using the **session_speakers** association table.

---

## Technologies Used

* Python 3
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* SQLAlchemy ORM
* SQLite

---

## Project Structure

```text
.
├── server/
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   └── ...
├── migrations/
├── Pipfile
├── Pipfile.lock
└── README.md
```

---

## Installation

1. Clone the repository.

```bash
git clone <git@github.com:wanja-juma/flask-sqlalchemy-relationships-lab.git>
cd <flask-sqlalchemy-relationships-lab>
```

2. Create and activate a virtual environment.

```bash
pipenv install
pipenv shell
```

3. Apply database migrations.

```bash
flask db upgrade
```

4. Seed the database.

```bash
python server/seed.py
```

5. Start the development server.

```bash
flask run
```

---

## API Endpoints

### Events

#### Get all events

```http
GET /events
```

Returns a list of all events.

Example response:

```json
[
  {
    "id": 1,
    "name": "Tech Conference",
    "location": "Nairobi"
  }
]
```

---

#### Get sessions for an event

```http
GET /events/<id>/sessions
```

Returns every session belonging to the specified event.

Example response:

```json
[
  {
    "id": 1,
    "title": "Introduction to Flask",
    "start_time": "09:00:00"
  }
]
```

If the event does not exist:

```json
{
  "error": "Event not found"
}
```

---

### Speakers

#### Get all speakers

```http
GET /speakers
```

Returns a list of all speakers.

Example response:

```json
[
  {
    "id": 1,
    "name": "Alice"
  }
]
```

---

#### Get a speaker and their biography

```http
GET /speakers/<id>
```

Example response:

```json
{
  "id": 1,
  "name": "Alice",
  "bio_text": "Senior Backend Engineer"
}
```

If a speaker has no biography:

```json
{
  "id": 2,
  "name": "Brian",
  "bio_text": "No bio available"
}
```

If the speaker does not exist:

```json
{
  "error": "Speaker not found"
}
```

---

### Sessions

#### Get speakers for a session

```http
GET /sessions/<id>/speakers
```

Returns all speakers assigned to the specified session.

Example response:

```json
[
  {
    "id": 1,
    "name": "Alice",
    "bio_text": "Senior Backend Engineer"
  },
  {
    "id": 2,
    "name": "Brian",
    "bio_text": "No bio available"
  }
]
```

If the session does not exist:

```json
{
  "error": "Session not found"
}
```

---

## HTTP Status Codes

| Status Code | Description                      |
| ----------- | -------------------------------- |
| 200         | Request completed successfully   |
| 404         | Requested resource was not found |

---

### Display Image

assets\Screenshot 2026-07-24 150602.png

## Author

Developed using Flask and SQLAlchemy to demonstrate relational database modeling and RESTful API development.
