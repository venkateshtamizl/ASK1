import threading
import time
import json
from pymodbus.client import ModbusTcpClient
from exo_decoder import ExoDecoder  # Import decoding logic from second script

# Modbus server details
HOST = '10.30.250.220'
PORT = 8899

# Create a Modbus TCP client
client = ModbusTcpClient(HOST, port=PORT)
stop_thread = False  # Flag to stop the thread

# Initialize decoder
decoder = ExoDecoder()

def read_modbus_registers():
    """ Continuously read Modbus registers, decode, and print as JSON """
    global client, stop_thread
    while not stop_thread:
        if not client.connected:
            print("Reconnecting to Modbus server...")
            client.connect()

        if client.connected:
            result = client.read_input_registers(address=0, count=100)
            if result is None or (hasattr(result, "isError") and result.isError()):
                print("Error reading registers")
            else:
                # Decode registers into meaningful sensor data
                sensor_data = decoder.decode_registers(result.registers)
                json_data = json.dumps(sensor_data, indent=4)
                print(json_data)

        time.sleep(2)  # Adjust polling interval as needed 

# Start the Modbus reading thread
modbus_thread = threading.Thread(target=read_modbus_registers, daemon=True)
modbus_thread.start()

try:
    while True:
        time.sleep(1)  # Keep the main program running
except KeyboardInterrupt:
    print("Stopping Modbus client...")
    stop_thread = True
    client.close()
