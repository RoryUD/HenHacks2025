import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from flask import Flask, jsonify, send_file
from sklearn.linear_model import LinearRegression
from matplotlib import colors

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def calculate_wind_speed(pressure, P_env=1013):
    """
    Calculate wind speed based on central pressure.
    """
    try:
        pressure = float(pressure)
        if np.isnan(pressure) or pressure <= 0:
            return None
        
        wind_speed_knots = 10 * np.sqrt(P_env - pressure)
        wind_speed_mps = wind_speed_knots * 0.514  # Convert knots to m/s
        
        return wind_speed_mps
    except ValueError:
        return None

@app.route('/api/hurricane-data', methods=['GET'])
def get_hurricane_data():
    try:
        file_path = "2005-2006.csv"  # Update with actual path
        df = pd.read_csv(file_path)
        
        if 'Date' not in df.columns or 'Pressure' not in df.columns:
            return jsonify({"error": "Required columns 'Date' or 'Pressure' not found"}), 400
        
        df.columns = df.columns.str.strip()
        df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d%H')
        df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
        df.dropna(subset=['Pressure', 'Date'], inplace=True)
        
        df['Wind Speed (m/s)'] = df['Pressure'].apply(calculate_wind_speed)
        
        if df.empty:
            return jsonify({"error": "No valid data after cleaning"}), 400

        # Prepare data for scatter plot and line of best fit
        X = df['Pressure'].values.reshape(-1, 1)  # Independent variable (Pressure)
        y = df['Wind Speed (m/s)'].values  # Dependent variable (Wind Speed)

        # Create a linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate the line of best fit
        y_pred = model.predict(X)

        # Define a pressure threshold (e.g., 950 hPa) for which we'll show the color bar
        pressure_threshold = 950
        df_filtered = df[df['Pressure'] >= pressure_threshold]

        # Generate scatter plot with Pressure on x-axis and Wind Speed on y-axis
        plt.figure(figsize=(12, 6))
        
        # Extract the year from the Date column for coloring
        df_filtered['Year'] = df_filtered['Date'].dt.year

        # Normalize the year values for color mapping
        norm = colors.Normalize(vmin=df_filtered['Year'].min(), vmax=df_filtered['Year'].max())
        scatter = plt.scatter(df_filtered['Pressure'], df_filtered['Wind Speed (m/s)'], 
                              c=df_filtered['Year'], cmap='viridis', norm=norm, label='Data Points', alpha=0.7)

        # Plot the line of best fit with Pressure on x-axis and predicted Wind Speed on y-axis
        plt.plot(df['Pressure'], y_pred, label='Line of Best Fit', color='red', linewidth=2)
        
        # Set limits for the y-axis (Wind Speed)
        plt.ylim(0, df['Wind Speed (m/s)'].max() * 1.1)  # Adjust to wind speed max range
        
        # Add color bar to show the year scale
        cbar = plt.colorbar(scatter, ax=plt.gca(), orientation='vertical')
        cbar.set_label('Year')

        # Label the axes and title
        plt.xlabel('Pressure (hPa)')
        plt.ylabel('Wind Speed (m/s)')
        plt.title('Pressure vs Wind Speed with Line of Best Fit')
        plt.legend()
        plt.grid(True)

        # Add annotations to the scatter points
        for i, txt in enumerate(df_filtered['Year']):
            plt.annotate(str(txt), (df_filtered['Pressure'].iloc[i], df_filtered['Wind Speed (m/s)'].iloc[i]),
                         fontsize=8, color='black', alpha=0.7, ha='right')

        plt.tight_layout()

        # Save the plot to a temporary file and send it
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp_file.name)
        plt.close()
        
        return send_file(temp_file.name, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": f"Failed to process data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
