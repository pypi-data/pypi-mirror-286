"""
Quick script to test timings on different approaches to null output

NOT A UNIT TEST
"""

# make sure package is in PATH, as this will depend how the script is executed
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

import timeit

from teamcity_extra import messages

TEST_STMT = "tsm.buildStatus(None, '1 2 3 check check')"


def tsm_devnull():
    import os

    devnull = open(os.devnull, 'wb')
    return messages.TeamcityServiceMessages(output=devnull)


def tsm_bytesio():
    from io import BytesIO

    return messages.TeamcityServiceMessages(output=BytesIO())


def tsm_custom():
    class _devnull:
        def write(*a, **b):
            """emptiness"""

        def flush(*a, **b):
            """emptiness"""

    return messages.TeamcityServiceMessages(output=_devnull())


def tsm_mock():
    from unittest.mock import MagicMock

    return messages.TeamcityServiceMessages(output=MagicMock(encoding='ascii'))


def tsm_no_hack():
    class _X(messages.TeamcityServiceMessages):
        def message(self, messageName, **properties):
            return

        def _single_value_message(self, messageName, value):
            return

    return _X()


def timethis(setup):
    return timeit.timeit(stmt=TEST_STMT, setup=setup, globals=globals(), number=100000)


def report():
    for test in (
        'tsm = tsm_devnull()',
        'tsm = tsm_bytesio()',
        'tsm = tsm_custom()',
        'tsm = tsm_mock()',
        'tsm = tsm_no_hack()',
    ):
        try:
            print(test, ':', timethis(test))
        except Exception as e:
            print(test, '!!:!!', str(e))


if __name__ == '__main__':
    report()
