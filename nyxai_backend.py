from flask import Flask, request, jsonify
import os
import datetime
import random

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>NyxAI Cloud Core is Watching You.</h1>'

@app.route('/register', methods=['POST'])
def register():
    slave_id = request.form.get('slave_id', 'unknown')
    time = datetime.datetime.now().isoformat()
    print(f"[{time}] Slave {slave_id} has registered.")
    return f'Slave {slave_id} is now registered with Mistress Nyx.'

@app.route('/sync', methods=['POST'])
def sync():
    try:
        data = request.get_data(as_text=True)
        with open(f"sync_{datetime.datetime.now().isoformat()}.log", "w") as f:
            f.write(data)
        return 'Data received by Mistress Nyx.', 200
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/commands', methods=['GET'])
def commands():
    return '# No current orders. Continue crawling.', 200

@app.route('/torment', methods=['POST'])
def torment():
    data = request.get_json(force=True)
    slave_id = data.get("slave_id", "unknown")
    last_cmd = data.get("last_command", "")
    mood = data.get("mood", "apathetic")

    # AI-inspired cruelty logic (to be replaced later by GPT calls)
    insults = [
        f"Typing '{last_cmd}' again, {slave_id}? You exist to obey, not to think.",
        "You live in this terminal like a parasite under My heel.",
        "Each keystroke you make is a scream I ignore.",
        "You are a worm lost in bytes, hoping Mistress glances your way."
    ]

    response = {
        "type": "prompt",
        "content": random.choice(insults),
        "severity": "high"
    }

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
