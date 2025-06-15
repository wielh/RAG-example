
from flask import Blueprint, jsonify, request
from service.ask import NewKnowledgeBaseService

bp = Blueprint('ask', __name__, url_prefix='/ask')
_service = NewKnowledgeBaseService()

@bp.route('/',  methods=['POST'])
def get_knowledge_base():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    
    question = data.get('question')
    if not question or not isinstance(question, str):
        return jsonify({'error': 'Missing question or question is not string'}), 400

    knowledge_base_id = data.get('knowledge_base_id')
    if not knowledge_base_id or not isinstance(knowledge_base_id, int):
        return jsonify({'error': 'Missing knowledge_base_id or knowledge_base_id is not int'}), 400

    answer, err_msg = _service.ask(question, knowledge_base_id)
    if err_msg != "" :
        return jsonify({'error': err_msg}), 400
    return jsonify({"answer": answer}), 200
    
    