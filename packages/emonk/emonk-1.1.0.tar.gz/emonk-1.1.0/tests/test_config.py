import os.path
import tempfile
import unittest

import emonk.config
import emonk.dialog


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        emonk.config.HOME = self.dir.name

    def test_setup(self):
        # Mock out dialog.
        path = os.path.join(self.dir.name, "journal.txt")

        def welcome():
            return dict(path=path)

        emonk.dialog.welcome = welcome
        config_path = os.path.join(self.dir.name, ".emonk")
        self.assertFalse(os.path.exists(config_path))
        # 1st read creates config file.
        emonk.config.read()
        self.assertEqual(emonk.config.get("path"), path)
        self.assertTrue(os.path.exists(config_path))
        # 2nd read verifies config file.
        config = emonk.config.read()
        self.assertEqual(emonk.config.get("path"), path)

    def tearDown(self):
        self.dir.cleanup()


if __name__ == "__main__":
    unittest.main()
