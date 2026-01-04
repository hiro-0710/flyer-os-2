from dataclasses import dataclass, field
from typing import List


@dataclass
class Utterance:
    role: str
    content: str


@dataclass
class ShortTermMemory:
    history: List[Utterance] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.history.append(Utterance(role=role, content=content))


memory = ShortTermMemory()
