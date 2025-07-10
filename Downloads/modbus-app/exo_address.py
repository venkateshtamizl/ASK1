class ExoRegisterAddress:
    def __init__(self):
        self.Translator_Status = 0
        self.Translator_Version = 2
        self.EXO_Error_Code = 4
        self.EXO_Status_Timestamp = 8
        self.EXO_Unit_ID = 10
        self.EXO_Battery_Level = 12
        self.EXO_Charging_Status = 14
        self.GPS_Latitude = 16
        self.GPS_Longitude = 18
        self.GPS_Altitude = 20
        self.GPS_Beacon_ID = 22
        self.Network_Signal_Strength = 24
        self.EXO_Alarm_Status = 26
        self.Reserved_for_future_use_1 = 28
        self.Reserved_for_future_use_2 = 30
        self.EXO_Measurement_Timestamp = 32
        self.Temperature = 34
        self.Pressure = 36
        self.Humidity = 38
        self.Next_Bump_Due = 40
        self.Pump_Active_Inlet = 42
        self.Pump_Flow_Rate = 44
        self.Reserved_for_future_use_3 = 46
        self.Reserved_for_future_use_4 = 48
        self.GS1_Status = 50
        self.GS1_Type = 52
        self.GS1_Reading = 54
        self.GS1_Units = 56
        self.GS1_Next_Calibration_Due = 58
        self.GS2_Status = 60
        self.GS2_Type = 62
        self.GS2_Reading = 64
        self.GS2_Units = 66
        self.GS2_Next_Calibration_Due = 68
        self.GS3_Status = 70
        self.GS3_Type = 72
        self.GS3_Reading = 74
        self.GS3_Units = 76
        self.GS3_Next_Calibration_Due = 78
        self.GS4_Status = 80
        self.GS4_Type = 82
        self.GS4_Reading = 84
        self.GS4_Units = 86
        self.GS4_Next_Calibration_Due = 88
        self.GS5_Status = 90
        self.GS5_Type = 92
        self.GS5_Reading = 94
        self.GS5_Units = 96
        self.GS5_Next_Calibration_Due = 98

        self.statusMask = 0x00000800  # This mask is derived to check if that particular sensor is active

        self.gasName = {
            0: "FRESH_AIR",
            1: "H2S",
            2: "CO",
            3: "O2",
            4: "CO2",
            5: "LEL",
            6: "N2",
            7: "NH3",
            8: "SO2",
            9: "CL2",
            10: "VOC_PPM",
            11: "HCN",
            12: "H2",
            13: "CLO2",
            14: "O3",
            15: "VOC_PPB",
            16: "NO2",
            17: "NN_LEL",
            18: "HF",
        }
        self.gasUnit = {0: "PPM", 1: "VOL", 2: "LE", 3: "MM3"}

        self.response_mapper_translator = [
            {
                "exo_response_code": 0x0001,
                "emc_response_code": "EXO1001",
                "exo_response_message": "No incoming messages in last 5s.",
            },
            {
                "exo_response_code": 0x0002,
                "emc_response_code": "EXO1002",
                "exo_response_message": "Latest message had invalid checksum.",
            },
            {
                "exo_response_code": 0x0004,
                "emc_response_code": "EXO1003",
                "exo_response_message": "Latest message could not be parsed.",
            },
        ]
        self.response_mapper_alarm = [
            {
                "exo_response_code": 0x0001,
                "emc_response_code": "EXO1101",
                "exo_response_message": "Emergency alert",
            },
            {
                "exo_response_code": 0x0002,
                "emc_response_code": "EXO1102",
                "exo_response_message": "Pump low flow warning",
            },
            {
                "exo_response_code": 0x0004,
                "emc_response_code": "EXO1103",
                "exo_response_message": "Cartridge error warning",
            },
            {
                "exo_response_code": 0x0008,
                "emc_response_code": "EXO1104",
                "exo_response_message": "Cartridge not recognized",
            },
            {
                "exo_response_code": 0x0010,
                "emc_response_code": "EXO1105",
                "exo_response_message": "Message warning",
            },
            {
                "exo_response_code": 0x0020,
                "emc_response_code": "EXO1106",
                "exo_response_message": "Incoming call warning",
            },
            {
                "exo_response_code": 0x0040,
                "emc_response_code": "EXO1107",
                "exo_response_message": "Comms lost warning",
            },
            {
                "exo_response_code": 0x0080,
                "emc_response_code": "EXO1108",
                "exo_response_message": "Low battery warning",
            },
            {
                "exo_response_code": 0x0100,
                "emc_response_code": "EXO1109",
                "exo_response_message": "Hardware test fail alarm",
            },
            {
                "exo_response_code": 0x0200,
                "emc_response_code": "EXO1110",
                "exo_response_message": "Firmware not certified warning",
            },
            {
                "exo_response_code": 0x0400,
                "emc_response_code": "EXO1111",
                "exo_response_message": "Pump failure alarm",
            },
            {
                "exo_response_code": 0x0800,
                "emc_response_code": "EXO1112",
                "exo_response_message": "Tipped over warning",
            },
        ]

        self.baseAddress = 0
        self.totalRegisters = 100
        self.functionCode = 4
