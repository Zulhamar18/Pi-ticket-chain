from flask import Blueprint, jsonify
from app.models.ticket import Ticket

tickets = Blueprint("tickets", __name__)

@tickets.route("/tickets", methods=["GET"])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([{"id": ticket.id, "event_id": ticket.event_id, "price": ticket.price} for ticket in tickets])