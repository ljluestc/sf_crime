from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Load data
    data_path = os.path.join("data", "sf_crime.csv")
    if not os.path.exists(data_path):
        return "<h3>No data found. Please run fetch_data.py or schedule an update.</h3>"

    df = pd.read_csv(data_path)

    # Create category counts for bar chart
    category_counts = df['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']

    # Create crime data dictionary for map (limit to 1000 points per category for performance)
    crime_data = {}
    for category in df['Category'].unique():
        cat_df = df[df['Category'] == category][['X', 'Y']].dropna()
        if len(cat_df) > 1000:
            cat_df = cat_df.sample(1000, random_state=42)
        crime_data[category] = {
            'lon': cat_df['X'].tolist(),
            'lat': cat_df['Y'].tolist()
        }

    # Render template with data
    return render_template("index.html", category_counts=category_counts, crime_data=crime_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)