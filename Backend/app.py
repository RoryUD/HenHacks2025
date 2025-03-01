# app.py (Flask)
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React to make requests

@app.route('/api/graph-data', methods=['GET'])
def get_graph_data():
    # Example graph data: number of disasters per Waffle House location
    graph_data = {
        "labels": ["Waffle House A", "Waffle House B", "Waffle House C", "Waffle House D"],
        "data": [5, 8, 2, 3]  # Corresponding disaster counts
    }
    return jsonify(graph_data)

if __name__ == "__main__":
    app.run(debug=True)
