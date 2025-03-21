#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common import ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

class DeviceDataManager(IDataMessageListener):
    def __init__(self):
        self.configUtil = ConfigUtil()

        self.enableSystemPerf = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.ENABLE_SYSTEM_PERF_KEY, defaultVal=True)

        self.enableSensing = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.ENABLE_SENSING_KEY, defaultVal=True)

        self.enableActuation = True

        self.sysPerfMgr = None
        self.sensorAdapterMgr = None
        self.actuatorAdapterMgr = None

        if self.enableSystemPerf:
            self.sysPerfMgr = SystemPerformanceManager()
            self.sysPerfMgr.setDataMessageListener(self)
            logging.info("System performance tracking enabled.")

        if self.enableSensing:
            self.sensorAdapterMgr = SensorAdapterManager()
            self.sensorAdapterMgr.setDataMessageListener(self)
            logging.info("Sensor tracking enabled.")

        if self.enableActuation:
            self.actuatorAdapterMgr = ActuatorAdapterManager()
            self.actuatorAdapterMgr.setDataMessageListener(self)
            logging.info("Actuation capabilities enabled.")

        self.handleTempChangeOnDevice = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY, defaultVal=True)

        self.triggerHvacTempFloor = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY, defaultVal=18.0)

        self.triggerHvacTempCeiling = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY, defaultVal=20.0)

    def startManager(self):
        logging.info("Starting DeviceDataManager...")
        
        if self.sysPerfMgr:
            self.sysPerfMgr.startManager()

        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.startManager()

        logging.info("DeviceDataManager started.")

    def stopManager(self):
        logging.info("Stopping DeviceDataManager...")
        
        if self.sysPerfMgr:
            self.sysPerfMgr.stopManager()

        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.stopManager()

        logging.info("DeviceDataManager stopped.")

    def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
        logging.info("Handling actuator command message: %s", str(data))

        if data:
            return self.actuatorAdapterMgr.sendActuatorCommand(data)
        else:
            logging.warning("Invalid actuator command received.")
            return None

    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        logging.info("Handling actuator command response: %s", str(data))
        return True

    def handleIncomingMessage(self, resourceEnum, msg: str) -> bool:
        logging.info("Handling incoming message: resource=%s, msg=%s", resourceEnum, msg)
        return True

    def handleSensorMessage(self, data: SensorData) -> bool:
        logging.info("Handling sensor data: %s", str(data))
        self._handleSensorDataAnalysis(data)
        return True

    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        logging.info("Handling system performance data: %s", str(data))
        return True

    def _handleSensorDataAnalysis(self, data: SensorData):
        if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
            logging.info("Analyzing temperature data: %s", data.getValue())

            ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)

            if data.getValue() > self.triggerHvacTempCeiling:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempCeiling)
            elif data.getValue() < self.triggerHvacTempFloor:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempFloor)
            else:
                ad.setCommand(ConfigConst.COMMAND_OFF)

            self.handleActuatorCommandMessage(ad)
