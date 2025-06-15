from enum import Enum

from llm.protocol import LLMInterface
from llm.ollama_openchat import OllamaLLM

class LLMModelOption(Enum):
   OLLAMA_OPENCHAT = "ollama_openchat"
   
def llm_selector(option: str) -> LLMInterface:
    match option:
        case LLMModelOption.OLLAMA_OPENCHAT.value:
            return OllamaLLM()
        case _:
            return OllamaLLM()