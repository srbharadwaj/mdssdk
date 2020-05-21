import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.constants import BASIC, ENHANCED
from mdssdk.devicealias import DeviceAlias, InvalidMode
from tests.test_device_alias.da_vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasAttrMode(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.oldmode = self.d.mode

    def test_mode_read(self):
        self.assertIn(self.d.mode.lower(), [BASIC, ENHANCED])

    def test_mode_write(self):
        if self.d.mode.lower() == BASIC:
            self.d.mode = ENHANCED
            self.assertEqual(ENHANCED, self.d.mode.lower())
            try:
                self.d.mode = BASIC
                self.assertEqual(BASIC, self.d.mode.lower())
            except CLIError as c:
                if "Device-alias enhanced zone member present" in c.message:
                    self.skipTest("Device-alias enhanced zone member present, so we cant change mode to basic")
        else:
            try:
                self.d.mode = BASIC
                self.assertEqual(BASIC, self.d.mode.lower())
            except CLIError as c:
                if "Device-alias enhanced zone member present" in c.message:
                    self.skipTest("Device-alias enhanced zone member present, so we cant change mode to basic")
            self.d.mode = ENHANCED
            self.assertEqual(ENHANCED, self.d.mode.lower())
        self.d.mode = self.oldmode
        self.assertEqual(self.oldmode, self.d.mode.lower())

    def test_mode_write_invalid(self):
        mode = 'asdf'
        with self.assertRaises(InvalidMode) as e:
            self.d.mode = mode
        self.assertEqual(
            "InvalidMode: Invalid device alias mode: " + str(mode) + ". Valid values are " + ENHANCED + "," + BASIC,
            str(e.exception))

    def tearDown(self) -> None:
        self.d.mode = self.oldmode
        self.assertEqual(self.oldmode.lower(), self.d.mode.lower())