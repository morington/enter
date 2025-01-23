import unittest
import tempfile
import os

import structlog

from src.core.domain.exceptions import ConfigHandlerError
from src.infrastructure.services.config import ConfigHandler


class TestConfigHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir.name)

        structlog.configure(
            processors=[],
            logger_factory=lambda *args, **kwargs: structlog.testing.CapturingLogger()
        )

    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def test_config_creation(self):
        """Checking for file creation if missing."""
        self.assertFalse(os.path.exists("config.ini"))
        ConfigHandler()
        self.assertTrue(os.path.exists("config.ini"))

    def test_missing_section(self):
        """The absence of an ENTER section causes an error."""
        with open("config.ini", "w") as f:
            f.write("[OTHER_SECTION]\nkey=value\n")

        with self.assertRaises(ConfigHandlerError):
            ConfigHandler()

    def test_missing_field(self):
        """Missing a required field causes an error."""
        with open("config.ini", "w") as f:
            f.write("[ENTER]\nyaml_file_path = test\n")

        with self.assertRaises(ConfigHandlerError):
            ConfigHandler()

    def test_empty_values(self):
        """Empty values cause an error on retrieval."""
        with open("config.ini", "w") as f:
            f.write("[ENTER]\nyaml_file_path = \nlang = \n")

        config = ConfigHandler()
        with self.assertRaises(ConfigHandlerError):
            _ = config.yaml_file_path
        with self.assertRaises(ConfigHandlerError):
            _ = config.lang

    def test_valid_config(self):
        """Correct values are returned correctly."""
        with open("config.ini", "w") as f:
            f.write("[ENTER]\nyaml_file_path = /test/path\nlang = en\n")

        config = ConfigHandler()
        self.assertEqual(config.yaml_file_path, "/test/path")
        self.assertEqual(config.lang, "en")


if __name__ == "__main__":
    unittest.main()