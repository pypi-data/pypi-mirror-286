import faulthandler
import logging
import os
import signal
import tempfile
from typing import Callable


def sample_stackframe_on_signal(
    signum: int = signal.SIGUSR2,
    handler: Callable[[int, object], None] = None,
    logger: logging.Logger = None,
) -> None:
    new_handler = handler
    if new_handler is None:

        def _handler(signum2, _frame):
            sig = signal.Signals(signum2)
            logger.debug(f"Signal {sig.name} received. Producing stack frame at ...")
            with tempfile.TemporaryFile() as f:
                stack = _sample_stackframe(f)
                logger.debug(f"Stack frame data:\n{stack}")
                logger.debug(
                    f"Alternatively invoke for more details: austin (or austin-ui) --pid={os.getpid()} --children --where={os.getpid()}"
                )

        new_handler = _handler

    old_handler = signal.getsignal(signum)

    def _wrapper_handler(signum2, _frame):
        new_handler(signum2, _frame)

        if old_handler == signal.SIG_IGN:
            pass
        elif callable(old_handler):
            old_handler(signum2, _frame)
        elif old_handler == signal.SIG_DFL:
            logger.debug(f"Default handler for signal {signal.Signals(signum2)} cannot be executed")
        else:
            logger.debug(f"Handler for signal {signal.Signals(signum2)} cannot be executed")

    signal_registered = signal.signal(signum, _wrapper_handler)
    logger.debug(
        f"Registered signal {signum}/{signal_registered}. Handler will produce the current process's stack frame for all threads"
    )


def _sample_stackframe(file) -> str:
    faulthandler.dump_traceback(file=file, all_threads=True)
    file.seek(0)

    def _decode(line: bytes) -> str:
        return line.decode("utf-8")

    return "".join(map(_decode, file.readlines()))
