
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List
from abc import ABC, abstractmethod

from common.decorator import singleton

class EmbeddingModel(ABC):
    @abstractmethod
    def embedding(self, str) -> List[float]:
        pass

@singleton
class MiniLMEmbeddingModel(ABC):
    def __init__(self):
        model_path = Path(__file__).resolve().parent.parent.parent / "embedding_model"/"all-MiniLM-L6-v2"
        self.model = SentenceTransformer(str(model_path))

    def embedding(self, content:str) -> List[float]:
        embeddings = self.model.encode([content])
        return embeddings[0].tolist()


   
