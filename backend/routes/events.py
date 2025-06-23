from flask import Blueprint, jsonify
from app.models.event import Event

events = Blueprint("events", __name__)

@events.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([{"id": event.id, "name": event.name, "date": event.date} for event in events])