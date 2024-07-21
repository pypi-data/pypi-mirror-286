import json

class SaveToJson:
  """A class for saving data to JSON files."""

  def __init__(self, file_path):
    """Initializes the class with the target file path.

    Args:
      file_path: The path to the file where the data will be saved.
    """
    self.file_path = file_path

  def save(self, data):
    """Saves the provided data to the specified file in JSON format.

    Args:
      data: The data to be saved (any Python object that can be serialized to JSON).

    Raises:
      Exception: If an error occurs during the saving process.
    """
    try:
      with open(self.file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4, default=str)
      print(f"Data successfully saved to {self.file_path}")
    except Exception as e:
      print(f"An error occurred while saving to {self.file_path}: {e}")
