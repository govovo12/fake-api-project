import json

def write_json(data: dict, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
