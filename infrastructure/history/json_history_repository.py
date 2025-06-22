import os
import json
import uuid
from typing import Optional
from dataclasses import asdict

from domain.model.chat_history import ChatHistory
from domain.model.role_message import RoleMessage
from domain.port.driven.chat_history_persistence_port import ChatHistoryPersistencePort

class JsonHistoryRepository(ChatHistoryPersistencePort):
    def __init__(self, storage_folder: str):
        self.storage_folder = storage_folder
        os.makedirs(self.storage_folder, exist_ok=True)

    def get_all_conversations(self) -> list[str]:
        files = os.listdir(self.storage_folder)
        return [file.split('.')[0] for file in files if file.endswith('.json')]

    def create_conversation(self) -> str:
        new_conversation_id = str(uuid.uuid4())
        file_path = os.path.join(self.storage_folder, f"{new_conversation_id}.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(ChatHistory(messages=[])), file, ensure_ascii=False, indent=4)
        return new_conversation_id

    def get_history(self, conversation_guid: str) -> Optional[ChatHistory]:
        file_path = os.path.join(self.storage_folder, f"{conversation_guid}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            messages = [RoleMessage(**msg) for msg in data.get('messages', [])]
            return ChatHistory(messages)

    def add_message_to_history(self, conversation_guid: str, role_message: RoleMessage) -> Optional[ChatHistory]:
        chat_history = self.get_history(conversation_guid)
        if chat_history is None:
            return None
        chat_history.messages.append(role_message)
        file_path = os.path.join(self.storage_folder, f"{conversation_guid}.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(chat_history), file, ensure_ascii=False, indent=4)
        return self.get_history(conversation_guid)

    def clear_history(self, conversation_guid: str) -> Optional[ChatHistory]:
        file_path = os.path.join(self.storage_folder, f"{conversation_guid}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(asdict(ChatHistory(messages=[])), file, ensure_ascii=False, indent=4)
        return self.get_history(conversation_guid)
