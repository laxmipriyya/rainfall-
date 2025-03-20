from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual weather API key
API_KEY = "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"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route("/predict_rainfall", methods=["GET"])
def predict_rainfall():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    
    # Fetch weather data
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(WEATHER_API_URL, params=params)
    data = response.json()
    
    if response.status_code != 200:
        return jsonify({"error": data.get("message", "Failed to fetch weather data")}), response.status_code
    
    # Extract relevant weather data
    weather_conditions = data.get("weather", [{}])[0].get("main", "Unknown")
    precipitation = data.get("rain", {}).get("1h", 0)  # Rain volume in the last hour (mm)
    
    # Simple rainfall prediction
    if "rain" in weather_conditions.lower() or precipitation > 0:
        prediction = "Rain is likely. Carry an umbrella!"
    else:
        prediction = "No significant rain expected."
    
    return jsonify({
        "city": city,
        "weather": weather_conditions,
        "precipitation": precipitation,
        "prediction": prediction
    })

if __name__ == "__main__":
    app.run(debug=True)
