from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Example data (replace with your dynamic data source)
markers = [
    {"name": "Ambedkar Memorial Park", "lat": 26.8500, "lng": 80.9499},
    {"name": "Chota Imambara (Hussainabad Imambara)", "lat": 26.8696, "lng": 80.9147},
    {"name": "Lucknow City Center (Hazratganj)", "lat": 26.8465108, "lng": 80.9466832}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/markers')
def get_markers():
    return jsonify(markers)

if __name__ == '__main__':
    app.run(debug=True)
