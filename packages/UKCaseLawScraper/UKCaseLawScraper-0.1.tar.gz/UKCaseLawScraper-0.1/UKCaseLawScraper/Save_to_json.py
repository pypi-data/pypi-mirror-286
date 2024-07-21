import json

class SaveToJson:
    @staticmethod
    def save(data, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4, default=str)
            print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving to {file_path}: {e}")
