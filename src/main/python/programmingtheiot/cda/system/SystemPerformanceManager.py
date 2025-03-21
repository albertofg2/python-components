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
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask
from apscheduler.schedulers.background import BackgroundScheduler

class SystemPerformanceManager():
    
    def __init__(self):
        self.configUtil = ConfigUtil()
        self.pollRate = self.configUtil.getInteger(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.POLL_CYCLES_KEY,
            ConfigConst.DEFAULT_POLL_CYCLES)

        self.locationID = self.configUtil.getProperty(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.DEVICE_LOCATION_ID_KEY,
            ConfigConst.NOT_SET)

        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        self.dataMsgListener = None

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)

    def handleTelemetry(self):
        self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        self.memUtilPct = self.memUtilTask.getTelemetryValue()

        logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.',
                      str(self.cpuUtilPct), str(self.memUtilPct))

        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.setCpuUtilization(self.cpuUtilPct)
        sysPerfData.setMemoryUtilization(self.memUtilPct)

        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(data=sysPerfData)

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        return False

    def startManager(self):
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("SystemPerformanceManager scheduler started.")
        else:
            logging.info("Scheduler already running.")

    def stopManager(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("SystemPerformanceManager scheduler stopped.")
        else:
            logging.info("Scheduler already stopped.")
