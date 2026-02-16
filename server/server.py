from flask import Flask, request, jsonify
import paho.mqtt.publish as publish

app = Flask(__name__)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883

MQTT_TOPIC = 'drone/telemetry'

# Store last received telemetry
last_telemetry = None



# POST handler for telemetry
@app.route('/telemetry', methods=['POST'])
def receive_telemetry():
    global last_telemetry
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload received'}), 400
    print(f"Received telemetry: {data}")  # Log received data
    last_telemetry = data
    # Publish to MQTT
    publish.single(MQTT_TOPIC, payload=str(data), hostname=MQTT_BROKER, port=MQTT_PORT)
    return jsonify({'status': 'Telemetry received'}), 200

# GET handler for telemetry info/testing
@app.route('/telemetry', methods=['GET'])
def telemetry_info():
    if last_telemetry:
        return f'<h2>Telemetry endpoint is running.<br>Last received telemetry:</h2><pre>{last_telemetry}</pre>'
    else:
        return '<h2>Telemetry endpoint is running.<br>No telemetry data received yet.</h2>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
