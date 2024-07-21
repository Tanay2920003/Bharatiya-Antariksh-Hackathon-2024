from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    # Example endpoint that returns JSON data
    data = {
        "message": "Hello from Flask!",
        "status": "success"
    }
    return jsonify(data)

@app.route('/api/echo', methods=['POST'])
def echo():
    # Example POST endpoint that echoes back the data sent
    json_data = request.get_json()
    return jsonify(json_data)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    return f"Hello, {username}!"

if __name__ == '__main__':
    app.run(debug=True)
