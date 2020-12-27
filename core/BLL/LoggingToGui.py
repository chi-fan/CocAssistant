# -*- coding: utf-8 -*-
from logging.handlers import QueueHandler, QueueListener
import logging
from .QtUtils import SendLoggingToQt

class LoggingToGui (QueueListener) :
    def __init__(self, queue, m_sendLogging) :
        self._sendLogging = m_sendLogging
        super(LoggingToGui, self).__init__(queue)
        self.formatter = logging.Formatter(
            fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
            datefmt='%I:%M:%S'
        )
        
    def handle(self, record) :
        record = self.prepare(record)
        if not self.respect_handler_level:
            process = True
        else:
            process = record.levelno >= handler.level
        if process:
            self._sendLogging.sendLog(self.formatter.format(record))