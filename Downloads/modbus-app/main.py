import threading
import time
import json
from fastapi import FastAPI
from pymodbus.client import ModbusTcpClient
from exo_decoder import ExoDecoder
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for stricter access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modbus server details
HOST = '10.30.250.220'
PORT = 8899

# Create a Modbus TCP client
client = ModbusTcpClient(HOST, port=PORT)

# Initialize decoder
decoder = ExoDecoder()

# Shared variable for storing sensor data
sensor_data = {}

def read_modbus_registers():
    """ Continuously read Modbus registers and store decoded data """
    global client, sensor_data
    while True:
        if not client.connected:
            print("Reconnecting to Modbus server...")
            client.connect()

        if client.connected:
            result = client.read_input_registers(address=0, count=100)
            if result is None or (hasattr(result, "isError") and result.isError()):
                print("Error reading registers")
            else:
                sensor_data = decoder.decode_registers(result.registers)

        time.sleep(2)  # Adjust polling interval as needed

# Start Modbus reading thread
modbus_thread = threading.Thread(target=read_modbus_registers, daemon=True)
modbus_thread.start()

@app.get("/")
def root():
    return {"message": "Modbus API is running!"}

@app.get("/data")
def get_sensor_data():
    return sensor_data
