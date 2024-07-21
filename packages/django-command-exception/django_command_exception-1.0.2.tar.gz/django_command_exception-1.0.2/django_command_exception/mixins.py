__all__ = [
    "CommandException",
]

import time
import traceback

from .models import CommandException

class CommandExceptionMixin:

    def error(self, e):
        CommandException(
            command = type(self).__module__.split('.')[-1],
            exc_class = type(e),
            exc_message = str(e),
            exc_traceback = ''.join(traceback.format_tb(e.__traceback__)),
            created_at = int(time.time())
        ).save()
