import logging

logging.VERBOSE = 5

logging._levelToName[logging.VERBOSE] = 'VERBOSE'
logging._nameToLevel['VERBOSE'] = logging.VERBOSE


def verbose(self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.VERBOSE):
        self._log(logging.VERBOSE, msg, *args, **kwargs)
setattr(logging.Logger, 'verbose', verbose)
