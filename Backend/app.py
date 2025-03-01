import pandas as pd
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/hurricane-data', methods=['GET'])
def get_hurricane_data():
    # Correct file path using raw string literal or forward slashes
    try:
        # Use raw string (r"") or forward slashes (/) for file path
        df = pd.read_csv(r"2005-2006.csv")  # Use the correct path
        print(df)  # Optionally print the dataframe to debug
        # Perform any necessary processing on the data, e.g., filtering by year, location, etc.
        print("Current working directory:", os.getcwd())
        return jsonify(df.to_dict(orient='records'))  # Convert to a list of dictionaries
    except Exception as e:
        return jsonify({"error": f"Failed to load or process data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
