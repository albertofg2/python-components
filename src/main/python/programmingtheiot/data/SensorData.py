#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
    """
    Representa datos simples de un sensor con soporte para valores flotantes.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        super(SensorData, self).__init__(name=name, typeID=typeID, d=d)
        
        # Inicializamos con valor por defecto
        self.value = ConfigConst.DEFAULT_VAL

    def getValue(self) -> float:
        return self.value

    def setValue(self, newVal: float):
        self.value = newVal
        self.updateTimeStamp()  # actualiza timestamp al cambiar el valor

    def _handleUpdateData(self, data):
        if data and isinstance(data, SensorData):
            self.value = data.getValue()

    def __str__(self):
        return (f"SensorData [name={self.getName()}, typeID={self.getTypeID()}, value={self.value}, "
                f"timeStamp={self.getTimeStamp()}]")
