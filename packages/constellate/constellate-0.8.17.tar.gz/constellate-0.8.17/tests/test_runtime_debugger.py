import logging
import signal

from pyexpect import expect

from constellate.logger.handler.stringhandler import StringHandler
from constellate.runtime.debugger.debugger import run_debugger_on_signal


def test_debugger_on_signal() -> None:
    handler = StringHandler(capacity=0)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Register signal handler
    sig = signal.SIGUSR2
    run_debugger_on_signal(signum=sig.value, logger=logger, debugger_wait=False)

    # Send signal
    signal.raise_signal(sig)

    text = handler.output()
    expect(text).to_contain("Waiting for debugger client")
    expect(text).to_contain("Debugger client connected")
