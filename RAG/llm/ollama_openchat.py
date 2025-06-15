from langchain_ollama import ChatOllama
from typing import List
from common.decorator import singleton
from llm.protocol import LLMInterface
from langchain.schema import HumanMessage

@singleton
class OllamaLLM(LLMInterface):
    def __init__(self, model_opt: str = "openchat"):
        self.llm = ChatOllama(model=model_opt, temperature=0.3)
        self.system_instruction = """
            1. 你是一個根據參考文獻，統整、總結並回答問題的助手。
            2. 請用上你的智慧，判斷哪些文件與問題相關，參考後統整，做出回答，而不是只是返回某個文獻。
            3. 請只關注與問題本身有相關的內容，而忽略其他部分。
            4. 請用繁體中文回答。 
            5. 如果無法從資料中得到答案，請回答「資料中沒有相關資訊」。
        """
    
    def ask(self, question:str, reference_content_list: List[str]) -> str:
        reference_content = "\n\n".join([f"文獻 {i+1}:\n{content}\n\n" for i, content in enumerate(reference_content_list)])
        full_prompt = f"""
        系統提示:
        {self.system_instruction}

        問題：
        {question}

        參考文獻：
        {reference_content}
        """

        print("=============================")
        print(full_prompt)
        response = self.llm.invoke(full_prompt)
        return response.content
