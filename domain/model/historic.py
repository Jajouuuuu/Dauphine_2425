class Historic:
    def __init__(self):
        self.list_message = []

    def add_message(self, message: str):
        self.list_message.append(message)

    def __str__(self):
        return str(self.list_message)