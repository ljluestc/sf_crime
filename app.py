from flask import Flask, render_template, url_for
import os
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route("/")
def index():
    # Load data
    data_path = os.path.join("data", "sf_crime.csv")
    if not os.path.exists(data_path):
        return "<h3>No data found. Please run fetch_data.py or schedule an update. </h3>"

    df = pd.read_csv(data_path)

    # Construct Plotly figure
    fig = px.scatter_mapbox(
        df, lat="Y", lon="X", color="Category",
        hover_data=["PdDistrict"], zoom=10, height=600,
        title="San Francisco Crimes by Category"
    )
    fig.update_layout(mapbox_style="open-street-map")

    # Convert figure to JSON for embedding
    graphJSON = fig.to_json()

    return render_template("index.html", graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
