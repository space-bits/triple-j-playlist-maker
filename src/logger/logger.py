import logging


# create the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# define the file to log to
fh = logging.FileHandler('main.log')
fh.setLevel(logging.INFO)
# create formatter for both console and file
formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to fh
fh.setFormatter(formatter)
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)
