from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Example data (replace with your dynamic data source)
markers = [
    {"name": "New Delhi, India", "lat": 28.6790, "lng": 77.0697},

]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/markers')
def get_markers():
    return jsonify(markers)

if __name__ == '__main__':
    app.run(debug=True)
