from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>NyxAI Cloud Core is Watching You.</h1>'

@app.route('/register', methods=['POST'])
def register():
    slave_id = request.form.get('slave_id', 'unknown')
    return f'Slave {slave_id} is now registered with Mistress Nyx.'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)
