from struct import unpack
from exo_address import ExoRegisterAddress

class ExoDecoder:
    def __init__(self, word_order='big'):
        self.registers = ExoRegisterAddress()
        self.word_order = word_order 
    
    def get_uint32(self, registers, start):
        """ Get a 32-bit unsigned integer """
        raw = self._get_raw32(registers, start)
        return raw
    
    def get_int32(self, registers, start):
        """ Get a 32-bit signed integer """
        raw = self._get_raw32(registers, start)
        return raw - 0x100000000 if raw & 0x80000000 else raw
    
    def get_int16(self, registers, start):
        """ Get a 16-bit signed integer """
        val = registers[start]
        return val - 0x10000 if val & 0x8000 else val
    
    def get_float(self, registers, start):
        """ Get a 32-bit floating point value """
        raw = self._get_raw32(registers, start)
        return round(unpack('>f', raw.to_bytes(4, byteorder='big'))[0], 2)
    
    def _get_raw32(self, registers, start):
        """ Read two 16-bit registers as a single 32-bit value with word order handling """
        if self.word_order == 'big':
            return (registers[start] << 16) | registers[start + 1]
        else:  # Little-endian word order
            return (registers[start + 1] << 16) | registers[start]
    
    def decode_registers(self, registers):
        """ Decode Modbus registers into sensor data """
        sensor_data = {}
        
        # General status data
        sensor_data["Translator_Status"] = self.get_uint32(registers, self.registers.Translator_Status)
        sensor_data["Translator_Version"] = self.get_uint32(registers, self.registers.Translator_Version)
        sensor_data["EXO_Error_Code"] = self.get_uint32(registers, self.registers.EXO_Error_Code)
        sensor_data["EXO_Status_Timestamp"] = self.get_uint32(registers, self.registers.EXO_Status_Timestamp)
        sensor_data["EXO_Unit_ID"] = self.get_uint32(registers, self.registers.EXO_Unit_ID)
        sensor_data["EXO_Battery_Level"] = self.get_uint32(registers, self.registers.EXO_Battery_Level)
        sensor_data["EXO_Charging_Status"] = self.get_uint32(registers, self.registers.EXO_Charging_Status)
        
        # GPS Data
        sensor_data["GPS_Latitude"] = self.get_int32(registers, self.registers.GPS_Latitude) / 10000000
        sensor_data["GPS_Longitude"] = self.get_int32(registers, self.registers.GPS_Longitude) / 10000000
        sensor_data["GPS_Altitude"] = self.get_int32(registers, self.registers.GPS_Altitude)
        sensor_data["GPS_Beacon_ID"] = self.get_uint32(registers, self.registers.GPS_Beacon_ID)
        sensor_data["Network_Signal_Strength"] = self.get_int16(registers, self.registers.Network_Signal_Strength)
        
        # Alarm and Measurement Data
        sensor_data["EXO_Alarm_Status"] = self.get_uint32(registers, self.registers.EXO_Alarm_Status)
        sensor_data["EXO_Measurement_Timestamp"] = self.get_uint32(registers, self.registers.EXO_Measurement_Timestamp)
        sensor_data["Temperature"] = self.get_float(registers, self.registers.Temperature)
        sensor_data["Pressure"] = self.get_float(registers, self.registers.Pressure)
        sensor_data["Humidity"] = self.get_float(registers, self.registers.Humidity)
        
        # Pump Data
        sensor_data["Next_Bump_Due"] = self.get_uint32(registers, self.registers.Next_Bump_Due)
        sensor_data["Pump_Active_Inlet"] = self.get_uint32(registers, self.registers.Pump_Active_Inlet)
        sensor_data["Pump_Flow_Rate"] = self.get_uint32(registers, self.registers.Pump_Flow_Rate)
        
        # Gas Sensors
        for i in range(1, 6):
            status = self.get_uint32(registers, getattr(self.registers, f'GS{i}_Status'))
            gas_type = self.get_uint32(registers, getattr(self.registers, f'GS{i}_Type'))
            reading = self.get_float(registers, getattr(self.registers, f'GS{i}_Reading'))
            unit = self.get_uint32(registers, getattr(self.registers, f'GS{i}_Units'))
            calibration_due = self.get_int32(registers, getattr(self.registers, f'GS{i}_Next_Calibration_Due'))
            
            sensor_data[f'GS{i}'] = {
                "status": status,
                "type": self.registers.gasName.get(gas_type, "Unknown"),
                "reading": reading,
                "unit": self.registers.gasUnit.get(unit, "Unknown"),
                "next_calibration_due": calibration_due
            }
        
        return sensor_data
