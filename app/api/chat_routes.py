"""Chat API routes - RAG-powered chat with AI assistant"""
from flask import Blueprint, request
from app.services.chat_service import ChatService
from app.utils.response import success_response, error_response, handle_api_error


chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/sessions', methods=['POST'])
@handle_api_error
def create_chat_session():
    """
    Create a new mock chat session
    ---
    tags:
      - Chat
    parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Meal planning"
    responses:
      201:
        description: Session created successfully
    """
    data = request.get_json(silent=True) or {}
    session = ChatService.create_session(title=data.get('title'))
    return success_response(data=session, message='Chat session created successfully', status_code=201)


@chat_bp.route('/sessions', methods=['GET'])
@handle_api_error
def list_chat_sessions():
    """
    List mock chat sessions
    ---
    tags:
      - Chat
    responses:
      200:
        description: List of chat sessions
    """
    sessions = ChatService.list_sessions()
    return success_response(data=sessions, message='Chat sessions retrieved successfully')


@chat_bp.route('/sessions/<session_id>/messages', methods=['GET'])
@handle_api_error
def get_chat_messages(session_id):
    """
    Get chat messages by session ID
    ---
    tags:
      - Chat
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: Chat session UUID
    responses:
      200:
        description: Chat messages retrieved successfully
      404:
        description: Session not found
    """
    messages = ChatService.get_messages(session_id)
    return success_response(data=messages, message='Chat messages retrieved successfully')


@chat_bp.route('/sessions/<session_id>/messages', methods=['POST'])
@handle_api_error
def send_chat_message(session_id):
    """
    Send a message and get AI assistant reply using RAG
    ---
    tags:
      - Chat
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: Chat session UUID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - content
          properties:
            content:
              type: string
              example: "Tôi có trứng và cà chua, nấu gì được?"
            user_pantry:
              type: array
              items:
                type: string
              example: ["trứng", "cà chua", "hành lá"]
              description: "Nguyên liệu người dùng hiện có (optional)"
    responses:
      200:
        description: User and assistant messages returned
      400:
        description: Missing content
      404:
        description: Session not found
    """
    data = request.get_json(silent=True) or {}
    if 'content' not in data:
        return error_response('Missing required field: content', 400)

    payload = ChatService.send_message(
        session_id=session_id, 
        content=data.get('content'),
        user_pantry=data.get('user_pantry')
    )
    return success_response(data=payload, message='Message sent successfully')


@chat_bp.route('/sessions/<session_id>', methods=['DELETE'])
@handle_api_error
def delete_chat_session(session_id):
    """
    Delete a mock chat session
    ---
    tags:
      - Chat
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: Chat session UUID
    responses:
      200:
        description: Session deleted successfully
      404:
        description: Session not found
    """
    result = ChatService.delete_session(session_id)
    return success_response(data=result, message='Chat session deleted successfully')
