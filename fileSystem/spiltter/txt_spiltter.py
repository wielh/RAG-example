from pathlib import Path
from typing import List
from time import time

from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from common.decorator import singleton
from spiltter.protocol import TextSplitter, SplitResult, ParentChunkSplitResult, ChildrenChunkSplitResult

@singleton
class TxtFileSplitter(TextSplitter):
   
    def __init__(self):
        self.parentSplitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n"]
        )

        self.childSplitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            separators=["\n"]
        )

    def split_file(self, path:Path) -> SplitResult:
        loader = TextLoader(path, encoding='utf-8')
        documents = loader.load()  

        timestamp = int(time() * 1000)
        result = SplitResult(timestamp)
        parent_text = self.parentSplitter.split_documents(documents)

        for i, parent in enumerate(parent_text):
            content = parent.page_content
            parent_result = ParentChunkSplitResult(content=content, chunk_index=i)
            children = self.childSplitter.split_text(content)
            for j, child in enumerate(children):
                child_result = ChildrenChunkSplitResult(content=child, chunk_index=j)
                parent_result.child.append(child_result)
            result.parent.append(parent_result)
        return result
    
 


