#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):

    def __init__(self, dataMsgListener: IDataMessageListener = None):
        self.dataMsgListener = dataMsgListener

        self.configUtil = ConfigUtil()

        self.useEmulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.ENABLE_EMULATOR_KEY,
            defaultVal=True)

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
            # Instancia actuadores simulados
            self.humidifierActuator = HumidifierActuatorSimTask()
            self.hvacActuator = HvacActuatorSimTask()
        else:
            # Instancia actuadores emulados dinámicamente
            hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidifierEmulatorTask')
            hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
            self.humidifierActuator = hueClazz()

            hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
            hveClazz = getattr(hveModule, 'HvacEmulatorTask')
            self.hvacActuator = hveClazz()

            leDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
            leClazz = getattr(leDisplayModule, 'LedDisplayEmulatorTask')
            self.ledDisplayActuator = leClazz()

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
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
                    logging.warning("Invalid actuator type: %s", data.getTypeID())

                if actuatorResponse and self.dataMsgListener:
                    self.dataMsgListener.handleActuatorCommandResponse(actuatorResponse)

                return actuatorResponse
            else:
                logging.warning("Location ID mismatch: expected %s, got %s", self.locationID, data.getLocationID())
        else:
            logging.warning("Invalid actuator data or response flag is enabled.")

        return None
