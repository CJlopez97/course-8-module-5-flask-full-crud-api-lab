from flask import Flask, abort, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/")
def home():
  return jsonify(message="Welcome to the Events API!")

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
  data = request.get_json()

  if not data or "title" not in data:
    abort(400, description="Missing required field: title")

  new_id = events[-1].id + 1 if events else 1
  new_event = Event(id=new_id, title=data["title"])

  events.append(new_event)

  return jsonify(new_event.to_dict()), 201


# PATCH /events/<int:event_id> - Update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
  data = request.get_json()

  if not data or "title" not in data:
    abort(400, description="Missing required field: title for update")

  event = next((e for e in events if e.id == event_id), None)

  if event is None:
    abort(404, description=f"Event with id {event_id} not found")

  event.title = data["title"]
  return jsonify(event.to_dict())


# DELETE /events/<int:event_id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
  global events
  event = next((e for e in events if e.id == event_id), None)

  if event is None:
    abort(404, description=f"Event with id {event_id} not found")

  events = [e for e in events if e.id != event_id]

  return "", 204


if __name__ == "__main__":
  app.run(debug=True)