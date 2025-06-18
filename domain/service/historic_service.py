from infrastructure.history.json_history_repository import JsonHistoryRepository

class HistoricService:
    def __init__(self, history_repository: JsonHistoryRepository):
        self.history_repository = history_repository

    def add_message(self, message: str) -> None:
        """Add a message to the history"""
        try:
            self.history_repository.add_message(message)
        except Exception as e:
            print(f"Error adding message to history: {e}")

    def get_messages(self) -> list:
        """Get all messages from history"""
        try:
            return self.history_repository.get_messages()
        except Exception as e:
            print(f"Error getting messages from history: {e}")
            return []
