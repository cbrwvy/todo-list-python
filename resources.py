import json
import os


def print_with_indent(value, indent=0):
    indentation = " " * indent
    print(indentation + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries],
        }
        return res

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for x in value.get('entries', []):
            new_entry.add_entry(cls.from_json(x))
        return new_entry

    def save(self, path: str):
        content = self.json()
        with open(f'{path}/{self.title}.json', 'w', encoding='utf-8') as f:
            json.dump(content, f)

    @classmethod
    def load(cls, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
        return Entry.from_json(content)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            content = entry.json()
            with open(f'{self.data_path}/{entry.title}.json', 'w', encoding='utf-8') as f:
                json.dump(content, f)

    def load(self):
        for file_path in os.listdir(self.data_path):
            file_full_path = os.path.join(self.data_path, file_path)
            if file_full_path.endswith('.json'):
                entry = Entry.load(file_full_path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))
