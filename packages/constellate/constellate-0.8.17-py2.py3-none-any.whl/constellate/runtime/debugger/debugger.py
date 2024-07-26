import logging
import os
import signal
import debugpy

from constellate.runtime.signal.helper import (
    register_signal_handler,
    Signal,
    SignalHandler,
    SignalHandlerOverride,
)


def run_debugger_on_signal(
    signum: Signal = signal.SIGUSR2,
    handler: SignalHandler = None,
    logger: logging.Logger = None,
    debugger_port: int = 5678,
    debugger_wait: bool = True,
    mode: SignalHandlerOverride = SignalHandlerOverride.OVERRIDE_ALWAYS,
) -> None:
    new_handler = None
    if handler is not None:
        new_handler = handler
    else:

        def _handler(_signum2, _frame):
            _wait_for_debugger_client(port=debugger_port, logger=logger, wait=debugger_wait)

        new_handler = _handler

    register_signal_handler(signum=signum, handler=new_handler, logger=logger, mode=mode)


def _wait_for_debugger_client(
    port: int = -1, logger: logging.Logger = None, wait: bool = True
) -> None:
    logger.debug(f"Waiting for debugger client on {port}")
    logger.debug(f"To connect application PID {os.getpid()}: madbg connect 127.0.0.1 {port}'")
    debugpy.listen(port)
    if wait:
        debugpy.wait_for_client()
    logger.debug("Debugger client connected")
