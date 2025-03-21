#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import random

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet

class BaseSensorSimTask:
    """
    Clase base que simula generación de datos de sensor.
    """

    DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
    DEFAULT_MAX_VAL = 100.0

    def __init__(self, name: str = ConfigConst.NOT_SET,
                 typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE,
                 dataSet: SensorDataSet = None,
                 minVal: float = DEFAULT_MIN_VAL,
                 maxVal: float = DEFAULT_MAX_VAL):

        self.name = name
        self.typeID = typeID
        self.dataSet = dataSet
        self.minVal = minVal
        self.maxVal = maxVal

        self.dataSetIndex = 0
        self.latestSensorData = None

        # Usa datos aleatorios si no existe un dataset predefinido
        self.useRandomizer = dataSet is None

    def getName(self) -> str:
        return self.name

    def getTypeID(self) -> int:
        return self.typeID

    def generateTelemetry(self) -> SensorData:
        sensorData = SensorData(typeID=self.getTypeID(), name=self.getName())

        if self.useRandomizer:
            sensorVal = random.uniform(self.minVal, self.maxVal)
        else:
            sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
            self.dataSetIndex += 1

            # Reinicia índice al llegar al final
            if self.dataSetIndex >= self.dataSet.getDataEntryCount():
                self.dataSetIndex = 0

        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData

        return self.latestSensorData

    def getTelemetryValue(self) -> float:
        if not self.latestSensorData:
            self.generateTelemetry()

        return self.latestSensorData.getValue()
