import json
import re
import argparse
from typing import Any

def validate_variable_name(name: str) -> bool:
    return re.match(r"^[_a-zA-Z][_a-zA-Z0-9]*$", name) is not None

def to_config_value(value: Any) -> str:
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return f"[[{value}]]"
    elif isinstance(value, dict):
        return "{\n" + "\n".join(
            f"    {k} = {to_config_value(v)};" for k, v in value.items()
        ) + "\n}"
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

def evaluate_expression(expr: str) -> Any:
    expr = expr.strip('|')
    try:
        if 'ord(' in expr or 'chr(' in expr:
            return eval(expr)
        return eval(expr)
    except Exception as e:
        raise ValueError(f"Ошибка вычисления выражения: {expr}. {e}")

def json_to_config(data: dict) -> str:
    config_lines = []
    for key, value in data.items():
        if not validate_variable_name(key):
            raise ValueError(f"Недопустимое имя переменной: {key}")

        if isinstance(value, str) and value.startswith('|') and value.endswith('|'):
            evaluated_value = evaluate_expression(value)
            config_lines.append(f"{key} is {evaluated_value}")
        else:
            config_lines.append(f"{key} is {to_config_value(value)}")
    return "\n".join(config_lines)

def main():
    parser = argparse.ArgumentParser(description="JSON to Config Converter")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to output config file")
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as infile:
            json_data = json.load(infile)

        config_output = json_to_config(json_data)

        with open(args.output, 'w', encoding='utf-8') as outfile:
            outfile.write(config_output)

        print(f"Файл успешно преобразован и сохранён в {args.output}")

    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
    except ValueError as e:
        print(f"Ошибка преобразования: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()
