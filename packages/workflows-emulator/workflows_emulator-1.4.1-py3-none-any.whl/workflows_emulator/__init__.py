import logging

# add Google custom logging levels
logging.addLevelName(logging.INFO - 1, 'DEFAULT')
logging.addLevelName(logging.INFO + 5, 'NOTICE')
logging.addLevelName(logging.CRITICAL + 5, 'ALERT')
logging.addLevelName(logging.CRITICAL + 10, 'EMERGENCY')
