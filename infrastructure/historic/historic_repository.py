import json
from domain.model.historic import Historic
from domain.port.historic_port import HistoricRepository

class JsonHistoricRepository(HistoricRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, historic: Historic):
        try:
            with open(self.file_path, 'w') as f:
                json.dump({"messages": historic.list_message}, f)
        except Exception as e:
            print(f"Error saving historic: {e}")
            raise e

    def get(self, id: int) -> Historic:
        try:
            with open(self.file_path, 'r') as f:
                content = f.read().strip() 
                if not content:  
                    print(f"File {self.file_path} is empty.")
                    return Historic()  

                data = json.loads(content)  
                historic = Historic()
                historic.list_message = data["messages"]
                return historic
        except FileNotFoundError:
            print(f"File {self.file_path} not found. Returning empty historic.")
            return Historic()  
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {self.file_path}: {e}")
            return Historic()  
