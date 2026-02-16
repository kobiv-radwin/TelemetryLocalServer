import requests
import time
import subprocess
import sys
import os
import signal

def kill_existing_mosquitto():
    """Kill all running mosquitto.exe processes."""
    try:
        if os.name == 'nt':
            # Windows
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if 'mosquitto.exe' in line:
                    pid = int(line.split()[1])
                    subprocess.run(['taskkill', '/PID', str(pid), '/F'])
                    print(f'Killed mosquitto.exe with PID {pid}')
        else:
            # Unix
            result = subprocess.run(['pgrep', 'mosquitto'], capture_output=True, text=True)
            for pid in result.stdout.split():
                subprocess.run(['kill', '-9', pid])
                print(f'Killed mosquitto with PID {pid}')
    except Exception as e:
        print(f'Error killing mosquitto: {e}')

def start_mosquitto():
    try:
        subprocess.Popen([
            r'C:\Program Files\mosquitto\mosquitto.exe', '-v'
        ])
        print('Started Mosquitto broker.')
    except Exception as e:
        print(f'Could not start Mosquitto: {e}')

def start_http_server():
    try:
        # Use the venv python to start server.py
        server_proc = subprocess.Popen([
            os.path.join(os.path.dirname(sys.executable), 'python.exe'),
            'server.py'
        ])
        print('Started HTTP server.')
        return server_proc
    except Exception as e:
        print(f'Could not start HTTP server: {e}')
        return None

def start_mqtt_sub():
    try:
        return subprocess.Popen([
            r'C:\Program Files\mosquitto\mosquitto_sub.exe',
            '-v',  # verbose output
            '-h', 'localhost',
            '-t', 'drone/telemetry'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f'Could not start mosquitto_sub: {e}')
        return None

def send_telemetry():
    url = 'http://localhost:5000/telemetry'
    data = {"lat": 32.1, "lon": 34.8}
    try:
        response = requests.post(url, json=data)
        print('POST response:', response.status_code, response.text)
    except Exception as e:
        print(f'Error sending telemetry: {e}')

def main():
    print('Killing existing Mosquitto sessions...')
    kill_existing_mosquitto()
    time.sleep(1)

    print('Starting Mosquitto broker...')
    start_mosquitto()
    time.sleep(2)  # Give broker time to start

    print('Starting HTTP server...')
    server_proc = start_http_server()
    time.sleep(2)  # Give HTTP server time to start

    print('Starting MQTT subscriber...')
    sub_proc = start_mqtt_sub()
    time.sleep(2)  # Give subscriber time to connect

    print('Sending telemetry data to HTTP server...')
    send_telemetry()
    time.sleep(2)  # Wait for message to be received

    if sub_proc:
        print('MQTT subscriber output:')
        try:
            output, err = sub_proc.communicate(timeout=10)
            print('STDOUT:', output.decode(errors='ignore'))
            print('STDERR:', err.decode(errors='ignore'))
            if not output.strip():
                print('No output received from MQTT subscriber.')
        except subprocess.TimeoutExpired:
            sub_proc.kill()
            print('No output received from MQTT subscriber (timeout).')

    if server_proc:
        server_proc.terminate()
        print('Stopped HTTP server.')

if __name__ == '__main__':
    main()
