from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Example: Real-time bus movement API endpoint
BUS_API_URL = 'https://api.busses.lk/v1/realtime'

# In-memory storage for subscribed bus stops
subscribed_stops = []

@app.route('/api/stops', methods=['GET'])
def get_subscribed_stops():
    return jsonify(subscribed_stops)

@app.route('/api/stops', methods=['POST'])
def add_stop():
    stop_id = request.json.get('stop_id')
    if stop_id and stop_id not in subscribed_stops:
        subscribed_stops.append(stop_id)
    return jsonify(subscribed_stops)

@app.route('/api/stops', methods=['DELETE'])
def remove_stop():
    stop_id = request.json.get('stop_id')
    if stop_id in subscribed_stops:
        subscribed_stops.remove(stop_id)
    return jsonify(subscribed_stops)

@app.route('/api/bus-data', methods=['GET'])
def get_bus_data():
    try:
        response = requests.get(BUS_API_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        bus_data = response.json()
        return jsonify(bus_data)
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
