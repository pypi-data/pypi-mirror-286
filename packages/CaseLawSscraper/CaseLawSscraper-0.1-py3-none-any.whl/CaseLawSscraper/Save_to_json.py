import json

def save_to_json(self, data, file_path):
    """Saves the scraped data to a JSON file in a pretty-printed format.

    Args:
      data: The data to save.
      file_path: The path of the file to save the data to.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4, default=str)