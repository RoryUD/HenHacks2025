import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, jsonify, send_file
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
        print(df.head())  # Optionally print the dataframe to debug

        # Perform any necessary processing on the data, e.g., filtering by year, location, etc.
        print("Current working directory:", os.getcwd())
        
        # Assuming the CSV has 'Date' and 'Pressure' columns. Adjust column names as needed.
        if 'Date' not in df.columns or 'Pressure' not in df.columns:
            return jsonify({"error": "Required columns not found in the data"}), 400
        
        # Convert the 'Date' column to datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Drop rows where the date or pressure is missing
        df.dropna(subset=['Pressure', 'Date'], inplace=True)

        # Plotting the data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Pressure'], label='Pressure')
        plt.xlabel('Date')
        plt.ylabel('Pressure (hPa)')
        plt.title('Hurricane Pressure Over Time')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a file
        plot_path = "hurricane_pressure_plot.png"
        plt.savefig(plot_path)

        # Return the plot image to the user
        return send_file(plot_path, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": f"Failed to load or process data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
