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
from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask:
    """
    Clase base para simular actuadores en el CDA.
    """

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
        self.latestActuatorResponse = ActuatorData(typeID=typeID, name=name)
        self.latestActuatorResponse.setAsResponse()

        self.name = name
        self.typeID = typeID
        self.simpleName = simpleName
        self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
        self.lastKnownValue = ConfigConst.DEFAULT_VAL

    def getLatestActuatorResponse(self) -> ActuatorData:
        return self.latestActuatorResponse

    def getSimpleName(self) -> str:
        return self.simpleName

    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        if data and self.typeID == data.getTypeID():
            statusCode = ConfigConst.DEFAULT_STATUS

            curCommand = data.getCommand()
            curVal = data.getValue()

            if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
                logging.debug(
                    "El comando y valor del actuador son iguales a los anteriores. Ignorando: %s %s",
                    str(curCommand), str(curVal))
            else:
                logging.debug(
                    "Nuevo comando del actuador a aplicar: %s con valor %s",
                    str(curCommand), str(curVal))

                if curCommand == ConfigConst.COMMAND_ON:
                    logging.info("Activando actuador...")
                    statusCode = self._activateActuator(val=data.getValue(), stateData=data.getStateData())
                elif curCommand == ConfigConst.COMMAND_OFF:
                    logging.info("Desactivando actuador...")
                    statusCode = self._deactivateActuator(val=data.getValue(), stateData=data.getStateData())
                else:
                    logging.warning("Comando desconocido. Ignorando: %s", str(curCommand))
                    statusCode = -1

                self.lastKnownCommand = curCommand
                self.lastKnownValue = curVal

                actuatorResponse = ActuatorData()
                actuatorResponse.updateData(data)
                actuatorResponse.setStatusCode(statusCode)
                actuatorResponse.setAsResponse()

                self.latestActuatorResponse.updateData(actuatorResponse)

                return actuatorResponse

        return None

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        msg = "\n*******"
        msg += "\n* O N *"
        msg += "\n*******"
        msg += "\n" + self.name + " VALUE -> " + str(val) + "\n======="

        logging.info("Simulando activación del actuador %s: %s", self.name, msg)

        return 0

    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        msg = "\n*******"
        msg += "\n* OFF *"
        msg += "\n*******"

        logging.info("Simulando desactivación del actuador %s: %s", self.name, msg)

        return 0
