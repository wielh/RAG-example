from typing import List, Any
from abc import ABC, abstractmethod
from pathlib import Path

class ChildrenChunkSplitResult:
    chunk_index: int
    content: str
    def __init__(self, content:str, chunk_index: int):
        self.content = content
        self.chunk_index = chunk_index

class ParentChunkSplitResult:
    chunk_index: int
    content: str
    child: list[ChildrenChunkSplitResult]
    def __init__(self, content:str, chunk_index: int):
        self.content = content
        self.chunk_index = chunk_index
        self.child = []

class SplitResult:
    parent: list[ParentChunkSplitResult]
    timestamp: int
    def __init__(self, timestamp: int):
        self.parent = []
        self.timeStamp = timestamp

class TextSplitter(ABC):
    @abstractmethod
    def split_file(self, path: Path) -> SplitResult:
        pass

