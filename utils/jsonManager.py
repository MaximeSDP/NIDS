import json
import os

class JsonManager:
    

    @staticmethod
    def _load(nameFile:str):
        FILE_PATH = os.path.join(os.path.dirname(__file__), str(nameFile))
        if not os.path.exists(FILE_PATH):
            return {}
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    @staticmethod
    def _save(nameFile,data):
        FILE_PATH = os.path.join(os.path.dirname(__file__), str(nameFile))
        # Ensure the directory exists
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        
        try:
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving to {FILE_PATH}: {e}")
            return False

    @staticmethod
    def _clear(nameFile):
        """Clear all data from the JSON file (set to empty list)"""
        return JsonManager._save(nameFile, {})