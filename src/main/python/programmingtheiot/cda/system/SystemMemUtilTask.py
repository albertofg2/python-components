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

class SystemMemUtilTask(BaseSystemUtilTask):
    """
    Collects memory utilization metrics using the psutil library.
    """

    def __init__(self):
        # Llamamos al constructor de la clase base
        super(SystemMemUtilTask, self).__init__(name=ConfigConst.MEM_UTIL_NAME, typeID=ConfigConst.MEM_UTIL_TYPE)
    
    def getTelemetryValue(self) -> float:
        # Usamos psutil para obtener el porcentaje de uso de la memoria
        return psutil.virtual_memory().percent
