from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Example data (replace with your dynamic data source)
markers = [


]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/markers')
def get_markers():
    return jsonify(markers)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
