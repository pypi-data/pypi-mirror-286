import json
import os.path
from datetime import datetime

from prettytable import PrettyTable
from pydantic import Field, BaseModel


class History(BaseModel):
    command: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class CommandHistoryManager:
    def __init__(self):
        self.history = []

    def record(self, command: str):
        self.history.append(History(command=command))

    def print(self):
        hist_dict = {}

        for h in self.history:
            hist_dict[h.timestamp] = h.command

        cols = ["Time", "Command"]
        t = PrettyTable(cols)
        t.align[cols[0]] = "l"
        t.align[cols[1]] = "l"
        for k in hist_dict:
            t.add_row([k, hist_dict[k]])
        print(t)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            f.write(json.dumps([h.dict() for h in self.history], indent=4))

    def load(self, file_path: str):
        if not os.path.exists(file_path):
            return
        with open(file_path, 'r') as f:
            data = json.loads(f.read())
            self.history = [History(**h) for h in data]
