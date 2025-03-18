#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import psutil

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
import programmingtheiot.common.ConfigConst as ConfigConst

class SystemCpuUtilTask(BaseSystemUtilTask):
    """
    Collects CPU utilization metrics using the psutil library.
    """

    def __init__(self):
        # Llamamos al constructor de la clase base
        super(SystemCpuUtilTask, self).__init__(name=ConfigConst.CPU_UTIL_NAME, typeID=ConfigConst.CPU_UTIL_TYPE)
    
    def getTelemetryValue(self) -> float:
        # Usamos psutil para obtener el porcentaje de uso de la CPU
        return psutil.cpu_percent()
