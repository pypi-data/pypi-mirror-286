import os
import sys
import logging


def should_colorize(stream):
    if stream is None:
        return False

    if stream is sys.stdout or stream is sys.stderr:
        try:
            import ipykernel
            import IPython

            ipython = IPython.get_ipython()
            is_jupyter_stream = isinstance(stream, ipykernel.iostream.OutStream)
            is_jupyter_shell = isinstance(
                ipython, ipykernel.zmqshell.ZMQInteractiveShell
            )
        except Exception:
            pass
        else:
            if is_jupyter_stream and is_jupyter_shell:
                return True

    if stream is sys.__stdout__ or stream is sys.__stderr__:
        if "CI" in os.environ and any(
            ci in os.environ
            for ci in ["TRAVIS", "CIRCLECI", "APPVEYOR", "GITLAB_CI", "GITHUB_ACTIONS"]
        ):
            return True
        if "PYCHARM_HOSTED" in os.environ:
            return True
        if os.name == "nt" and "TERM" in os.environ:
            return True

    try:
        return stream.isatty()
    except Exception:
        return False


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945

    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)