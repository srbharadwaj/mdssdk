import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrCores(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_cores_read(self):
        log.debug("Cores " + str(self.switch.cores))
        self.skipTest("Needs to be fixed")

    def test_cores_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.cores = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
