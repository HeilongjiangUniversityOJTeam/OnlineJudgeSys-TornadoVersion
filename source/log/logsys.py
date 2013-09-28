# -*- coding:utf-8 -*-
import logging
import logging.config

logging.config.fileConfig("conf.ini")

#create logger
logger = logging.getLogger("OnlineJudgeSys")

#"application" code
# logger.debug("debug message")
# logger.info("info message")
# logger.warn("warn message")
# logger.error("error message")
# logger.critical("critical message")
#
# logHello = logging.getLogger("hello")
# logHello.info("Hello world!")
