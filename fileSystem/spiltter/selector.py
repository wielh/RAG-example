from enum import Enum
from spiltter.txt_spiltter import TxtFileSplitter
from spiltter.protocol import TextSplitter

class SplitterOption(Enum):
    TXT = "txt"

def splitter_selector(option: str) -> TextSplitter:
    match option:
        case SplitterOption.TXT.value:
            return TxtFileSplitter()
        case _:
            return TxtFileSplitter()
    