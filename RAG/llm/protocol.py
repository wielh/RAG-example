from abc import ABC, abstractmethod
from typing import List

class LLMInterface(ABC):
    @abstractmethod
    def ask(self, question:str, reference_content_list: List[str]) -> str:
        pass
