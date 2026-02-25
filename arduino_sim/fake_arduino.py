import socket
import json
import time
import random

# Setup the "Server" on Port 4000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 4000))
server.listen(1)

print("Fake Arduino is 'ON' and waiting for Streamlit on Port 4000...")

while True:
    conn, addr = server.accept()
    print(f"Streamlit connected from {addr}")
    try:
        while True:
            # Create the exact data structure your project needs
            data = {
                "sensor_id": 1,
                "density": round(random.uniform(1.0, 50.0), 2),
                "ph": random.randint(1, 14),
                "hardness": round(random.uniform(10.0, 100.0), 2),
                "rhelogy": round(random.uniform(0.0, 20.0), 2)
            }
            
            # Convert to JSON string and add a newline
            message = json.dumps(data) + "\n"
            conn.sendall(message.encode('utf-8'))
            
            print(f"Sent to Streamlit: {message.strip()}")
            time.sleep(2) # Send data every 2 seconds
    except (ConnectionResetError, BrokenPipeError):
        print("Streamlit disconnected. Waiting for new connection...")
    finally:
        conn.close()