# 專案介紹

## 簡介
這是用 python 寫的專案，包括兩大部分: fileSystem 是將文檔做成向量提供使用者搜尋；而 RAG 則是提供給使用者問問題，搜尋文檔後由AI總結。

## 使用到的技術
python, postgre with vector extension, embedding(all-MiniLM), llm(ollama - openchat 本地版), RecursiveCharacterTextSplitter

## 項目結構
+ file: 存放 fileSystem 檔案的地方
+ embedding_model: 存放 embedding_model的地方
+ table: 存放sql create table的script
+ fileSystem: 是將文檔做成向量提供使用者搜尋的地方。
    + 目前支援文字檔
    + 採用最基本的 RecursiveCharacterTextSplitter 分割文字
    + 將文檔分為 parent_chunk 與 children_chunk。parent_chunk 是給llm的參考文獻;
      而children_chunk則是用來向量搜尋的。
    + 分為 embedding_model, repository, splitter 部分。每個都實現實作與介面分離，方便日後新增新的選項。
+ RAG: 而 RAG 則是提供給使用者問問題，搜尋文檔後由AI總結。
    + 目前用  llm(ollama - openchat 本地版) 回答問題。
    + 分為 embedding_model, repository, llm 部分。每個都實現實作與介面分離，方便日後新增新的選項。
+ 本地還安裝 ollama - openchat 本地版

## TODO
+ fileSystem 與 RAG 共用程式放至 common
+ 考慮實作不同的 embedding_model。因為不同的 embedding_model 向量維度不同，所以考慮生成新的 knowledge_base 時
  創建不同的 table 以儲存不同的 embedding。
+ metadata 實作
