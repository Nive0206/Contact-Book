from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
DATA_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Ensure data is a dictionary
            if isinstance(data, dict):
                return data
            else:
                return {}  # If file contains a list or invalid, reset to empty dict
        except json.JSONDecodeError:
            return {}

# Save contacts
def save_contacts(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Get all contacts
@app.route("/get", methods=["GET"])
def get_contacts():
    return jsonify(load_contacts())

# Add a contact
@app.route("/add", methods=["POST"])
def add_contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    if not name or not phone:
        return jsonify({"error": "Name and Phone are required"}), 400
    contacts = load_contacts()
    if name in contacts:
        return jsonify({"error": "Contact already exists"}), 400
    contacts[name] = phone
    save_contacts(contacts)
    return jsonify({"message": "Contact added successfully!"})

# Update a contact
@app.route("/update", methods=["PUT"])
def update_contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    contacts = load_contacts()
    if name in contacts:
        contacts[name] = phone
        save_contacts(contacts)
        return jsonify({"message": "Contact updated successfully!"})
    return jsonify({"error": "Contact not found"}), 404

# Delete a contact
@app.route("/delete", methods=["DELETE"])
def delete_contact():
    data = request.get_json()
    name = data.get("name", "").strip()
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        return jsonify({"message": "Contact deleted successfully!"})
    return jsonify({"error": "Contact not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
