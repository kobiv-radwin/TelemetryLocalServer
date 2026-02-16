# Instructions for running the server and broker

## 1. Start the Mosquitto MQTT Broker
- Open a terminal (PowerShell or Command Prompt)
- Run the following command (adjust path if needed):

    "C:\Program Files\mosquitto\mosquitto.exe" -v

This will start the broker on port 1883 by default.

## 2. Start the Python HTTP Server
- In another terminal, navigate to the server directory:

    cd c:\Users\kobi_V\Documents\Drone_Read\server

- Run the server:

    ..venv\Scripts\python.exe server.py

## 3. Test the Setup
- Send a POST request to the HTTP server (e.g., using curl or Postman):

    curl -X POST http://<laptop-ip>:5000/telemetry -H "Content-Type: application/json" -d "{\"lat\":32.1,\"lon\":34.8}"

- The server will publish the data to the MQTT topic `drone/telemetry` on the local broker.

## 4. Subscribe to MQTT Topic (for testing)
- In a new terminal:

    "C:\Program Files\mosquitto\mosquitto_sub.exe" -h localhost -t drone/telemetry

You should see the telemetry data appear as it is received.

---

- Ensure the firewall allows connections on port 1883 (MQTT) and 5000 (HTTP).
- The HTTP server and MQTT broker must be running for the system to work.
