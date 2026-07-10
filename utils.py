import json
import os


def save_json(data, filename):
    os.makedirs("output", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)