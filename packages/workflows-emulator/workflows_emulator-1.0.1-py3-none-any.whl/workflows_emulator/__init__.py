import logging

import coloredlogs

# add Google custom logging levels
logging.addLevelName(logging.INFO - 1, 'DEFAULT')
logging.addLevelName(logging.INFO + 5, 'NOTICE')
logging.addLevelName(logging.CRITICAL + 5, 'ALERT')
logging.addLevelName(logging.CRITICAL + 10, 'EMERGENCY')
coloredlogs.install(
    fmt="[%(asctime)s] %(name)s [%(levelname)s] %(message)s",
    level='DEBUG',
    datefmt='%I:%M:%S',
)
