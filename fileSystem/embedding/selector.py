

from enum import Enum
from embedding.embedding import EmbeddingModel, MiniLMEmbeddingModel

class EmbeddingModelOption(Enum):
    MINI_LM = "mini_lm"
   
def embedding_selector(option: str) -> EmbeddingModel:
    match option:
        case EmbeddingModelOption.MINI_LM.value:
            return MiniLMEmbeddingModel()
        case _:
            return MiniLMEmbeddingModel()