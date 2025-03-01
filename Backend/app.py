import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hurricane-data', methods=['GET'])
def get_hurricane_data():
    # Example: Load and process hurricane data from a CSV file
    try:
        df = pd.read_csv('path_to_your_hurricane_data.csv')
        # Perform any necessary processing on the data, e.g., filtering by year, location, etc.
        # For simplicity, let's just return the data as JSON
        return jsonify(df.to_dict(orient='records'))  # Convert to a list of dictionaries
    except Exception as e:
        return jsonify({"error": f"Failed to load or process data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
