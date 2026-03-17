"""Mock chat service for frontend integration before real AI API is available."""
import uuid
from datetime import datetime, timezone


class ChatService:
    """In-memory chat service used to simulate assistant conversations."""

    _sessions = {}

    @staticmethod
    def _now_iso():
        """Return UTC timestamp in ISO8601 format."""
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def create_session(cls, title=None):
        """Create a new chat session."""
        session_id = str(uuid.uuid4())
        now = cls._now_iso()

        session = {
            'id': session_id,
            'title': title or 'New chat',
            'created_at': now,
            'updated_at': now,
            'messages': []
        }

        cls._sessions[session_id] = session
        return cls._serialize_session(session)

    @classmethod
    def list_sessions(cls):
        """List all chat sessions sorted by recent update."""
        sessions = sorted(
            cls._sessions.values(),
            key=lambda item: item['updated_at'],
            reverse=True
        )
        return [cls._serialize_session(session) for session in sessions]

    @classmethod
    def get_session(cls, session_id):
        """Get one chat session by id."""
        return cls._sessions.get(session_id)

    @classmethod
    def delete_session(cls, session_id):
        """Delete a chat session."""
        if session_id not in cls._sessions:
            raise ValueError(f"Chat session '{session_id}' not found")

        del cls._sessions[session_id]
        return {'message': 'Chat session deleted successfully'}

    @classmethod
    def get_messages(cls, session_id):
        """Get all messages in one session."""
        session = cls.get_session(session_id)
        if not session:
            raise ValueError(f"Chat session '{session_id}' not found")

        return session['messages']

    @classmethod
    def send_message(cls, session_id, content):
        """Append user message and generate a simulated assistant reply."""
        session = cls.get_session(session_id)
        if not session:
            raise ValueError(f"Chat session '{session_id}' not found")

        if not content or not content.strip():
            raise ValueError('Message content is required')

        now = cls._now_iso()

        user_message = {
            'id': str(uuid.uuid4()),
            'role': 'user',
            'content': content.strip(),
            'created_at': now
        }
        session['messages'].append(user_message)

        assistant_message = {
            'id': str(uuid.uuid4()),
            'role': 'assistant',
            'content': cls._build_mock_reply(content.strip()),
            'created_at': cls._now_iso()
        }
        session['messages'].append(assistant_message)

        session['updated_at'] = assistant_message['created_at']
        cls._auto_update_title(session)

        return {
            'session': cls._serialize_session(session),
            'user_message': user_message,
            'assistant_message': assistant_message
        }

    @staticmethod
    def _serialize_session(session):
        """Return session metadata for list/detail responses."""
        return {
            'id': session['id'],
            'title': session['title'],
            'created_at': session['created_at'],
            'updated_at': session['updated_at'],
            'message_count': len(session['messages'])
        }

    @staticmethod
    def _auto_update_title(session):
        """Set title from first user message when using default title."""
        if session['title'] != 'New chat':
            return

        for message in session['messages']:
            if message['role'] == 'user':
                truncated = message['content'][:40]
                session['title'] = truncated + ('...' if len(message['content']) > 40 else '')
                return

    @staticmethod
    def _build_mock_reply(content):
        """Create a deterministic fake assistant response for UI testing."""
        lowered = content.lower()

        if any(keyword in lowered for keyword in ['hello', 'hi', 'xin chao', 'chao']):
            return 'Xin chao! Toi la chatbot mock. Ban cu tiep tuc chat de FE test giao dien nhe.'

        if any(keyword in lowered for keyword in ['recipe', 'cong thuc', 'nau an']):
            return (
                'Goi y mock: Ban co the thu mon ga nuong mat ong. '
                'Buoc 1 uop ga 20 phut, buoc 2 nuong 25 phut o 200C.'
            )

        if any(keyword in lowered for keyword in ['ingredient', 'nguyen lieu', 'pantry']):
            return 'Mock response: Toi co the giup ban quan ly nguyen lieu va goi y mon tu pantry hien co.'

        return (
            'Day la phan hoi gia lap tu chat API. '
            'Ban co the dung response nay de test bubble chat, timestamp, va loading state.'
        )
