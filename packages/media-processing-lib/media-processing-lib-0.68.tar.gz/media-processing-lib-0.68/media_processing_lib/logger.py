"""
Python logger settings.
Uses ENv variables to control the log level:

YOUR_KEY_LOGLEVEL=4 python blabla.py
and logger.debug4("message")

"""
from loggez import make_logger
mpl_logger = make_logger("MPL")
