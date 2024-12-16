import json
import re
import argparse
import sys
import unittest

def parse_value(value):
    if isinstance(value, dict):
        return parse_dict(value)
    elif isinstance(value, str):
        return f"[[{value}]]"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

def parse_dict(d):
    if not d:
        return "{\n}\n"
    entries = []
    for key, value in d.items():
        if not re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', key):
            raise ValueError(f"Invalid identifier: {key}")
        entries.append(f"{key} = {parse_value(value)};")
    return "{\n" + "\n".join(entries) + "\n}"


def translate_json_to_config(json_data):
    if not isinstance(json_data, dict):
        raise ValueError("Root element of JSON must be an object.")
    return parse_dict(json_data)

def main():
    parser = argparse.ArgumentParser(description="JSON to Config Language Converter")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to output Config file")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        config_text = translate_json_to_config(json_data)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(config_text)

        print("Conversion completed successfully.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
