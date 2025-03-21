#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import json
import logging

from json import JSONEncoder
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil:
    def __init__(self, encodeToUtf8=False):
        self.encodeToUtf8 = encodeToUtf8
        logging.info("DataUtil instance created.")

    def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False):
        if not data:
            logging.debug("ActuatorData is null. Returning empty string.")
            return ""

        return json.dumps(data, indent=4, cls=JsonDataEncoder)

    def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False):
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning None.")
            return None

        jsonStruct = self._formatAndLoadDict(jsonData)
        ad = ActuatorData()
        self._updateIotData(jsonStruct, ad)
        return ad

    def sensorDataToJson(self, data: SensorData = None, useDecForFloat: bool = False):
        if not data:
            logging.debug("SensorData is null. Returning empty string.")
            return ""

        return json.dumps(data, indent=4, cls=JsonDataEncoder)

    def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False):
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning None.")
            return None

        jsonStruct = self._formatAndLoadDict(jsonData)
        sd = SensorData()
        self._updateIotData(jsonStruct, sd)
        return sd

    def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False):
        if not data:
            logging.debug("SystemPerformanceData is null. Returning empty string.")
            return ""

        return json.dumps(data, indent=4, cls=JsonDataEncoder)

    def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False):
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning None.")
            return None

        jsonStruct = self._formatAndLoadDict(jsonData)
        spd = SystemPerformanceData()
        self._updateIotData(jsonStruct, spd)
        return spd

    def _formatAndLoadDict(self, jsonData: str) -> dict:
        jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
        jsonStruct = json.loads(jsonData)
        return jsonStruct

    def _updateIotData(self, jsonStruct, obj):
        varStruct = vars(obj)
        for key in jsonStruct:
            if key in varStruct:
                setattr(obj, key, jsonStruct[key])
            else:
                logging.warning("Key '%s' not found in object.", key)

class JsonDataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
