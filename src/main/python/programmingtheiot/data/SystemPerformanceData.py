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

class SystemPerformanceData(BaseIotData):
    """
    Representa datos del rendimiento del sistema, incluyendo CPU y Memoria.
    """

    def __init__(self, d=None):
        super(SystemPerformanceData, self).__init__(
            name=ConfigConst.SYSTEM_PERF_MSG, 
            typeID=ConfigConst.SYSTEM_PERF_TYPE, 
            d=d
        )

        # Valores iniciales por defecto
        self.cpuUtil = ConfigConst.DEFAULT_VAL
        self.memUtil = ConfigConst.DEFAULT_VAL

    def getCpuUtilization(self) -> float:
        return self.cpuUtil

    def getMemoryUtilization(self) -> float:
        return self.memUtil

    def setCpuUtilization(self, cpuUtil: float):
        self.cpuUtil = cpuUtil
        self.updateTimeStamp()  # actualiza timestamp al cambiar uso CPU

    def setMemoryUtilization(self, memUtil: float):
        self.memUtil = memUtil
        self.updateTimeStamp()  # actualiza timestamp al cambiar uso Memoria

    def _handleUpdateData(self, data):
        if data and isinstance(data, SystemPerformanceData):
            self.cpuUtil = data.getCpuUtilization()
            self.memUtil = data.getMemoryUtilization()

    def __str__(self):
        return (f"SystemPerformanceData [name={self.getName()}, typeID={self.getTypeID()}, "
                f"cpuUtil={self.cpuUtil}, memUtil={self.memUtil}, timeStamp={self.getTimeStamp()}]")
