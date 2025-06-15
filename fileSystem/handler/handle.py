from pathlib import Path
import shutil
from embedding.selector import embedding_selector
from repository.file_chunking.protocol import ParentChunk, ChildrenChunk
from repository.file_chunking.selector import NewFileChunkingRepository
from spiltter.selector import splitter_selector

class FileHandler:
    
    def __init__(
        self, knowledge_base_id: int, source_path: Path, target_path: Path, embeddding_opt: str, 
        splitter_opt: str, accept_suffix: list[str]
    ):
        self.knowledge_base_id = knowledge_base_id
        self.source_path = source_path
        self.target_path = target_path
        self.embeddding_model = embedding_selector(embeddding_opt)
        self.splitter = splitter_selector(splitter_opt)
        self.accept_suffix = accept_suffix
        self.file_chunking_repo = NewFileChunkingRepository()

    def _process_file(self, path: Path):
        result = self.splitter.split_file(path)
        with self.file_chunking_repo.begin_transection() as (_, cur):
            file_id = self.file_chunking_repo.save_file(self.knowledge_base_id, str(path), cur)
            for r in result.parent:
                parent_chunk = ParentChunk()
                parent_chunk.index = r.chunk_index
                parent_chunk.content = r.content
                parent_chunk_id = self.file_chunking_repo.save_parent_chunk(file_id, parent_chunk, cur)
                children_chunk_list: list[ChildrenChunk] = [
                    ChildrenChunk(
                        s.chunk_index, 
                        s.content, 
                        self.embeddding_model.embedding(s.content)
                    ) for s in r.child
                ]
                self.file_chunking_repo.save_children_chunks(parent_chunk_id, children_chunk_list, cur)
     
    def spilt_files(self):
        for source_path in self.source_path.rglob("*"):  
            relative_path = source_path.relative_to(self.source_path)  
            target_path = self.target_path / relative_path
            print(f"current file: ${target_path}")
            if target_path.suffix.lower() in self.accept_suffix:
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, target_path.parent)
                except Exception as e:
                    print(f"error happens when we copy file to ${str(target_path)}:{e}")
                    continue
                try:
                    self._process_file(target_path)
                except Exception as e:
                    print(f"error happens when we split and save file:${str(target_path)}:{e}")
                    continue
