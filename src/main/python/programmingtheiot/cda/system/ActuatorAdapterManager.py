#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask

class ActuatorAdapterManager(object):

    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.dataMsgListener = dataMsgListener

        self.configUtil = ConfigUtil()

        self.useSimulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.ENABLE_SIMULATOR_KEY,
            defaultVal=True)

        self.useEmulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.ENABLE_EMULATOR_KEY,
            defaultVal=False)

        self.locationID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET)

        self.humidifierActuator = None
        self.hvacActuator = None
        self.ledDisplayActuator = None

        self._initEnvironmentalActuationTasks()

    def _initEnvironmentalActuationTasks(self):
        if not self.useEmulator:
            self.humidifierActuator = HumidifierActuatorSimTask()
            self.hvacActuator = HvacActuatorSimTask()

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        else:
            return False

    def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
        if data and not data.isResponseFlagEnabled():
            if data.getLocationID() == self.locationID:
                logging.info("Actuator command received for location ID %s. Processing...", data.getLocationID())

                actuatorResponse = None
                if data.getTypeID() == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
                    actuatorResponse = self.humidifierActuator.updateActuator(data)
                elif data.getTypeID() == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
                    actuatorResponse = self.hvacActuator.updateActuator(data)
                elif data.getTypeID() == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
                    actuatorResponse = self.ledDisplayActuator.updateActuator(data)
                else:
                    logging.warning("No valid actuator type found. Ignoring typeID: %s", data.getTypeID())

                if actuatorResponse and self.dataMsgListener:
                    self.dataMsgListener.handleActuatorCommandResponse(actuatorResponse)

                return actuatorResponse
            else:
                logging.warning("Location ID mismatch. Actuation ignored (me=%s, you=%s).", self.locationID, data.getLocationID())
        else:
            logging.warning("Invalid actuator data or response flag set. Ignoring command.")

        return None
