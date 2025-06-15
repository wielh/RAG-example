import threading
from flask import Blueprint, jsonify, request

from service.knowledge_base import NewKnowledgeBaseService

bp = Blueprint('knowledage_base', __name__, url_prefix='/knowledage_base')
_service = NewKnowledgeBaseService()
_execution_lock = threading.Lock()

@bp.route('/',  methods=['POST'])
def new_knowledge_base():
    def execute():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid or missing JSON'}), 400
        
        name = data.get('name')
        if not name or not isinstance(name, str):
            return jsonify({'error': 'Missing name or name is not string'}), 400
    
        splitter = data.get('splitter')
        if not splitter or not isinstance(splitter , str):
            return jsonify({'error': 'Missing splitter or splitter is not string'}), 400
        
        source_dir = data.get('source_dir')
        if not source_dir or not isinstance(source_dir , str):
            return jsonify({'error': 'Missing source_dir or source_dir is not string'}), 400

        suffix_list = data.get('suffix_list')
        if not isinstance(suffix_list, list) or not all(isinstance(suffix, str) for suffix in suffix_list):
            return jsonify({'error': 'suffix_list must be a list of string'}), 400
        
        embedding_model = data.get('embedding_model')
        if not isinstance(embedding_model,str):
            return jsonify({'error': 'embedding_model must be string'}), 400
        
        knowledge_base_id, err_msg = _service.new_knowledge_base(name, source_dir, embedding_model, splitter, suffix_list)
        if err_msg != "" :
            return jsonify({'error': err_msg}), 400
        return jsonify({'knowledge_base_id': knowledge_base_id}), 200

    if not _execution_lock.acquire(blocking=False):
        return jsonify({"error": "Another request is currently processing."}), 429
    try:
        result = execute()
    finally:
        _execution_lock.release()
    return result

@bp.route('/',  methods=['GET'])
def get_knowledge_base():
    id = request.args.get('id')
    name = request.args.get('name')
    if id is not None and isinstance(id, int):
        file_info, name, err_msg = _service.get_knowledge_base_info_by_id(id)
        if err_msg != "" :
            return jsonify({'error': err_msg}), 400
        return jsonify({"name":name, "file_info": dict(file_info)}),200
    elif name is not None and isinstance(name, str):
        file_info, id, err_msg = _service.get_knowledge_base_info_by_name(name)
        if err_msg != "" :
            return jsonify({'error': err_msg}), 400
        return jsonify({"id":id, "file_info": dict(file_info)}), 200
    
    return jsonify({'error': "Have to provide one of id:int or name:str"}), 400
    
    


