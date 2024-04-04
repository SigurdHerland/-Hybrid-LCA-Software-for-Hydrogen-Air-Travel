from flask import Flask, request, jsonify
from flask_cors import CORS
import Hybird


app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/flights', methods=['POST'])
def handle_flights():
    
    data = request.json
    flight_from = data.get('flightFrom')
    flight_to = data.get('flightTo')
    print(f"Received: From {flight_from} To {flight_to}")
    # Use the corrected function to get flight data
    flight_values = Hybird.node(flight_from, flight_to)
    print(flight_values)
    return jsonify(flight_values)  # Return the dynamic response based on input

if __name__ == '__main__':
    app.run(debug=True)
