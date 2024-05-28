import json
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')


def ensure_json_exists():
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)


def save_to_json(key, value):
    ensure_json_exists()
    with open(file_path, 'r') as file:
        data = json.load(file)

    data[key] = value

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_value_from_json(key):
    ensure_json_exists()
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data.get(key, None)
