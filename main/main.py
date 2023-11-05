import logging
import logging.config
import os
from datetime import datetime

import team_spirit

logging.config.fileConfig('logging.conf')

# Note that the name of name of the logger will be called "root"
logger = logging.getLogger()

# Create the logging directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create file handler for the logging
fh = logging.FileHandler(f'logs/{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log')
fh.setLevel(logging.DEBUG)
fh.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.addHandler(fh)

MAX_LOG_COUNT = 10

if __name__ == '__main__':
    files = os.listdir('logs')
    files = [os.path.join('logs', file) for file in files]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if len(files) > MAX_LOG_COUNT:
        logger.info(f'Found {len(files)} log files, exceeding MAX_LOG_COUNT of {MAX_LOG_COUNT}')
        logger.info('Removing old log files')
        for file in files[MAX_LOG_COUNT:]:
            os.remove(file)

    team_spirit.run()
