import json
import os


class File:
    def __init__(self, filename):
        self.filename = filename
        self._create_if_missing()

    def _create_if_missing(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def read(self):
        self._create_if_missing()

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except json.JSONDecodeError:
            print("File is damaged. Starting with empty data.")
            return []

    def write(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
