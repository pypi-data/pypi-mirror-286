import os.path
import tempfile
import unittest

import drakken.config as config


class TestConfig(unittest.TestCase):
    def test_json(self):
        s = """
{
    "CONFIG_TYPE": "JSON",
    "X": 42
}"""
        self.dir = tempfile.TemporaryDirectory()
        path = os.path.join(self.dir.name, "config.json")
        with open(path, "w") as f:
            f.write(s)
        cfg = config.load(path)
        self.assertEqual(config.get("CONFIG_TYPE"), "JSON")
        self.assertEqual(config.get("X"), 42)

    def test_yaml(self):
        s = """
    CONFIG_TYPE: YAML
    X: 101
"""
        self.dir = tempfile.TemporaryDirectory()
        path = os.path.join(self.dir.name, "config.yaml")
        with open(path, "w") as f:
            f.write(s)
        cfg = config.load(path)
        self.assertEqual(config.get("CONFIG_TYPE"), "YAML")
        self.assertEqual(config.get("X"), 101)

    def tearDown(self):
        self.dir.cleanup()


if __name__ == "__main__":
    unittest.main()
