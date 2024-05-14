from dataclasses import dataclass

@dataclass
class Country:
    CCode: int
    StateNme: str
    StateAbb: str

    def __str__(self):
        return f"{self.StateAbb} - {self.CCode} - {self.StateNme}"

    def __hash__(self):
        return hash(self.CCode)