import logging

logging.basicConfig()

def info_log(message):
   logger = logging.getLogger(__name__)
   logger.setLevel(logging.INFO)
   logger.info(message)

def debug_log(message):
   logger = logging.getLogger(__name__)
   logger.setLevel(logging.DEBUG)
   logger.debug(message)

def critical_log(message):
   logger = logging.getLogger(__name__)
   logger.setLevel(logging.CRITICAL)
   logger.debug(message)