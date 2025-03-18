#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import time  # Asegúrate de que esta importación esté al principio
from apscheduler.schedulers.background import BackgroundScheduler
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

# Configuración básica del logging para ver los mensajes
logging.basicConfig(level=logging.INFO)  # Esto permitirá que se muestren los mensajes de nivel INFO

class SystemPerformanceManager(object):
    """
    Shell representation of class for student implementation.
    """

    def __init__(self):
        logging.info("Initializing SystemPerformanceManager...")

        configUtil = ConfigUtil()

        self.pollRate = configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES
        )

        self.locationID = configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET
        )

        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

        self.dataMsgListener = None
        self.scheduler = BackgroundScheduler()

        # Instanciar las tareas de CPU y Memoria
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()

        logging.info("Created instance of ConfigUtil: %s", str(configUtil))

    def handleTelemetry(self):
        # Obtener valores de utilización de CPU y memoria
        cpuUtil = self.cpuUtilTask.getTelemetryValue()
        memUtil = self.memUtilTask.getTelemetryValue()

        # Crear el objeto de datos de rendimiento del sistema
        perfData = SystemPerformanceData(cpuUtil, memUtil)
        logging.info(f"SystemPerformanceManager - CPU: {cpuUtil:.2f}%, Memory: {memUtil:.2f}%")

        # Enviar datos al listener si está configurado
        if self.dataMsgListener:
            self.dataMsgListener.handleSensorMessage(perfData)

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        self.dataMsgListener = listener
        return True

    def startManager(self):
        logging.info("Starting SystemPerformanceManager.")
        # Agregar el trabajo al planificador para ejecutarlo a intervalos
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        self.scheduler.start()

    def stopManager(self):
        logging.info("Stopping SystemPerformanceManager.")
        self.scheduler.shutdown()

# Agregar esta parte para que no se cierre inmediatamente
if __name__ == '__main__':
    logging.info("Starting SystemPerformanceManager script...")  # Log al inicio
    perfMgr = SystemPerformanceManager()
    perfMgr.startManager()

    # Esperar 10 segundos antes de parar
    logging.info("Waiting for 10 seconds before stopping...")
    time.sleep(10)

    logging.info("Stopping SystemPerformanceManager...")
    perfMgr.stopManager()
    logging.info("SystemPerformanceManager stopped.")
