import unittest
import json
from main import validate_variable_name, to_config_value, evaluate_expression, json_to_config

class TestConfigTool(unittest.TestCase):
    def test_validate_variable_name(self):
        self.assertTrue(validate_variable_name("_validName"))
        self.assertTrue(validate_variable_name("a"))
        self.assertFalse(validate_variable_name("1invalid"))
        self.assertFalse(validate_variable_name("invalid-name"))

    def test_to_config_value(self):
        self.assertEqual(to_config_value(123), "123")
        self.assertEqual(to_config_value("text"), "[[text]]")
        self.assertEqual(
            to_config_value({"key": "value", "num": 42}),
            "{\n    key = [[value]];\n    num = 42;\n}"
        )

    def test_evaluate_expression(self):
        self.assertEqual(evaluate_expression("|1 + 2|"), 3)
        self.assertEqual(evaluate_expression("|ord('A')|"), 65)
        self.assertEqual(evaluate_expression("|chr(66)|"), "B")
        with self.assertRaises(ValueError):
            evaluate_expression("|invalid + expr|")

    def test_json_to_config(self):
        json_input = {
            "name": "example",
            "value": 42,
            "nested": {
                "key": "val"
            },
            "expression": "|10 + 5|"
        }
        expected_output = (
            "name is [[example]]\n"
            "value is 42\n"
            "nested is {\n    key = [[val]];\n}\n"
            "expression is 15"
        )
        self.assertEqual(json_to_config(json_input), expected_output)

    def test_json_to_config_invalid_name(self):
        json_input = {"1invalid": "value"}
        with self.assertRaises(ValueError):
            json_to_config(json_input)

if __name__ == "__main__":
    unittest.main()
