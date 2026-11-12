import tempfile
import unittest
from pathlib import Path

from assistant import Assistant, calculate


class CalculatorTests(unittest.TestCase):
    def test_precedence(self):
        self.assertEqual(calculate("2 + 3 * (4 - 1)"), 11)

    def test_unary(self):
        self.assertEqual(calculate("-5 + 2"), -3)

    def test_rejects_code(self):
        with self.assertRaises(ValueError):
            calculate("__import__('os').system('echo unsafe')")

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            calculate("10 / 0")


class AssistantTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.assistant = Assistant(Path(self.temp.name) / "notes.txt")

    def tearDown(self):
        self.temp.cleanup()

    def test_greeting(self):
        self.assertEqual(self.assistant.respond("hello"), "Hello! How can I help?")

    def test_calculation_command(self):
        self.assertEqual(self.assistant.respond("calculate 6 * 7"), "The answer is 42.")

    def test_notes_round_trip(self):
        self.assertEqual(self.assistant.respond("note finish README"), "I've saved your note.")
        self.assertIn("finish README", self.assistant.respond("read notes"))

    def test_unknown_command(self):
        self.assertIn("don't know", self.assistant.respond("fly to mars").lower())


if __name__ == "__main__":
    unittest.main()
