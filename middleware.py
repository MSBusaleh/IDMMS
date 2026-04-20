import serial
import json
import time

PORT = 'COM5'
BAUD = 115200
FILE_PATH = "../data.json"

def run_collector():
    while True:
        try:
            ser = serial.Serial(PORT, BAUD, timeout=1)

            while True:
                if ser.in_waiting <= 0: # i.e. no data
                    time.sleep(0.01)
                    continue
                
                line = ser.readline().decode('utf-8').strip()
                
            
                try:
                    data = json.loads(line)
                    data["received_at"] = time.time() # For your stale data check
                    data["rheology"] = data["pressure"] / data["density"] if data["density"] != 0 else 0 # Example calculation for rheology

                    with open("data.json", "w") as f:
                        json.dump(data, f)
                        
                    print(f"Data received and saved: {data}")
                        
                except json.JSONDecodeError:
                    print(f"Received non-JSON data: {line}")
                    continue
                
                time.sleep(0.01)

        except (serial.SerialException, serial.PortNotOpenError) as e:
            # 2. Handle the disconnection
            print(f"\nCONNECTION LOST: {e}")
            print("Retrying in 2 seconds... (Check USB cable)")
            time.sleep(2)
            continue

        except KeyboardInterrupt:
            print("\nShutting down collector.")
            break

if __name__ == "__main__":
    run_collector()