import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from flask import Flask, jsonify, send_file
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/hurricane-data', methods=['GET'])
def get_hurricane_data():
    try:
        # Load the dataset with full file path
        file_path = r"2005-2006.csv"  # Update this with the actual path
        print("Loading data from:", file_path)
        
        df = pd.read_csv(file_path)
        
        print(df.head())  # Check the first few rows of the data

        # Check if the necessary columns exist
        if 'Date' not in df.columns or 'Pressure' not in df.columns:
            return jsonify({"error": "Required columns 'Date' or 'Pressure' not found in the data"}), 400

        # Strip extra spaces from column names
        df.columns = df.columns.str.strip()

        # Convert 'Date' from 'YYYYMMDDHH' to datetime
        df['Date'] = pd.to_datetime(df['Date'].astype(str), format='%Y%m%d%H')

        # Convert 'Pressure' column to numeric, invalid parsing will be set to NaN
        df['Pressure'] = pd.to_numeric(df['Pressure'], errors='coerce')
        
        # Drop rows with NaN values in 'Pressure' or 'Date' columns
        df.dropna(subset=['Pressure', 'Date'], inplace=True)

        # Convert 'Date' to the number of days since the first hurricane date
        df['Date_num'] = (df['Date'] - df['Date'].min()).dt.days

        # Prepare features and target
        X = df[['Date_num']]  # Date_num as the feature (days since the start)
        y = df['Pressure']  # Pressure as the target

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train the linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate performance metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Prepare result
        result = {
            "Mean Squared Error": mse,
            "R-squared": r2,
            "Coefficients": model.coef_.tolist(),
            "Intercept": model.intercept_
        }

        # Print the results
        print("Model Results:")
        print(f"Mean Squared Error: {mse}")
        print(f"R-squared: {r2}")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")

        # Plotting the data as a scatter plot
        plt.figure(figsize=(20, 10))
        plt.scatter(df['Date'], df['Pressure'], label='Actual Pressure', color='blue', alpha=0.6)

        # Plot the regression line (predicted values)
        plt.plot(df['Date'], model.predict(df[['Date_num']]), label='Regression Line', color='red', linestyle='--')

        # Format the x-axis to show Date in 'YYYY-MM-DD' format
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Rotate the x-axis labels for better visibility
        plt.xticks(rotation=45)

        plt.xlabel('Date')
        plt.ylabel('Pressure (hPa)')
        plt.title('Hurricane Pressure Over Time - Scatter Plot with Regression Line')
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a file
        plot_path = "hurricane_pressure_regression_plot.png"
        plt.savefig(plot_path)

        # Return the plot image to the user
        return send_file(plot_path, mimetype='image/png')

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": f"Failed to load or process data: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
