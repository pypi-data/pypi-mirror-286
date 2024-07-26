import contextlib
import io
import time
from datetime import datetime
from unittest import TestCase

from teamcity_extra import messages


def fixed_time():
    return fixed_time._time


fixed_time._time = time.mktime(datetime(2000, 11, 2, 10, 23, 1).timetuple()) + 0.5569


class Test(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tsm_output = io.BytesIO()
        self.tsm = messages.TeamcityServiceMessages(output=self.tsm_output, now=fixed_time)

    def assertOutput(self, expected_output: str):
        self.assertEqual(
            self.tsm_output.getvalue(),
            expected_output.encode(),
        )

    def test_default_constructor(self):
        messages.TeamcityServiceMessages()

    def test_testMetadata(self):
        self.tsm.testMetadata('testName', 'link', value='https://github.com', type='link')
        self.assertOutput(
            "##teamcity[testMetadata timestamp='2000-11-02T10:23:01.556' name='link' testName='testName' type='link' value='https://github.com']\n",
        )

    def test_buildStatisticValue(self):
        self.tsm.buildStatisticValue('myVal', '1')
        self.assertOutput(
            "##teamcity[buildStatisticValue timestamp='2000-11-02T10:23:01.556' key='myVal' value='1']\n",
        )

    def test_addBuildTag(self):
        self.tsm.addBuildTag('customTag')
        self.assertOutput(
            "##teamcity[addBuildTag 'customTag']\n",
        )

    def test_removeBuildTag(self):
        self.tsm.removeBuildTag('customTag')
        self.assertOutput(
            "##teamcity[removeBuildTag 'customTag']\n",
        )

    def test_default_output(self):
        f = io.BytesIO()
        with contextlib.redirect_stdout(f):
            tsm = messages.TeamcityServiceMessages()
            tsm.removeBuildTag('customTag')
        self.assertEqual(
            f.getvalue(),
            b"##teamcity[removeBuildTag 'customTag']\n",
        )

    def test_no_output(self):
        f = io.BytesIO()
        with contextlib.redirect_stdout(f):
            tsm = messages.TeamcityServiceMessages(output=messages.NO_OUTPUT)
            tsm.removeBuildTag('customTag')
        self.assertEqual(
            f.getvalue(),
            b"",
        )
