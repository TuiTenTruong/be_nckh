"""Chat service - Calls food-ai-service for RAG-based chat"""
import os
import json
import uuid
from io import BytesIO
from datetime import datetime, timezone
from urllib import request as urlrequest
from urllib import error as urlerror
from flask import current_app

from app.models.recipe import Recipe


class ChatService:
    """Service for AI-powered chat using food-ai-service microservice."""

    # In-memory session storage for BE
    # Maps session_id -> { id, title, created_at, updated_at, messages }
    _sessions = {}

    @staticmethod
    def _get_ai_endpoint():
        """Get AI service chat endpoint"""
        base_url = (
            current_app.config.get('AI_SERVICE_BASE_URL')
            or os.getenv('AI_SERVICE_BASE_URL')
        )

        if base_url:
            base = base_url.rstrip('/')
            if base.endswith('/api/ai'):
                return f"{base}/chat"
            if base.endswith('/api/ai/chat'):
                return base
            return f"{base}/api/ai/chat"

        analyze_endpoint = (
            current_app.config.get('AI_SERVICE_ENDPOINT')
            or os.getenv('AI_SERVICE_ENDPOINT')
        )

        if analyze_endpoint:
            return analyze_endpoint.replace('/analyze-image', '/chat')

        return 'http://127.0.0.1:8000/api/ai/chat'
    
    @staticmethod
    def _now_iso():
        """Return UTC timestamp in ISO8601 format."""
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _get_recipes_for_context():
        """Get all recipes from database for RAG context"""
        try:
            recipes = Recipe.query.all()
            result = []
            for recipe in recipes:
                # Get ingredients through recipe_ingredients relationship
                ingredients = []
                for ri in recipe.recipe_ingredients:
                    if ri.ingredient:
                        ingredients.append({
                            "name": ri.ingredient.name,
                            "quantity": ri.quantity or '',
                            "unit": ri.unit or '',
                        })
                
                # Get steps as text
                steps_text = ""
                try:
                    steps_list = []
                    for step in recipe.steps.order_by('step_number'):
                        step_title = f"**{step.title}**" if step.title else ""
                        step_content = f"Bước {step.step_number}: {step_title} {step.description}"
                        if step.tip:
                            step_content += f" (Mẹo: {step.tip})"
                        steps_list.append(step_content)
                    steps_text = "\n".join(steps_list)
                except Exception:
                    steps_text = ""
                
                result.append({
                    "id": str(recipe.id),
                    "name": recipe.name,
                    "description": recipe.description or '',
                    "steps": steps_text,
                    "ingredients": ingredients,
                    "image_url": recipe.image_url,
                    "cook_time_minutes": recipe.cook_time_minutes,
                    "difficulty": recipe.difficulty,
                    "servings": recipe.servings
                })
            
            return result
        except Exception as e:
            print(f" [ChatService] Error getting recipes: {e}")
            import traceback
            traceback.print_exc()
            return []

    @classmethod
    def create_session(cls, title=None):
        """Create a new chat session."""
        session_id = str(uuid.uuid4())
        now = cls._now_iso()

        session = {
            'id': session_id,
            'title': title or 'Cuộc trò chuyện mới',
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
    def send_message(cls, session_id, content, user_pantry=None):
        """
        Send user message to AI service and get response.
        Uses RAG to find relevant recipes.
        """
        session = cls.get_session(session_id)
        if not session:
            raise ValueError(f"Chat session '{session_id}' not found")

        if not content or not content.strip():
            raise ValueError('Message content is required')

        now = cls._now_iso()

        # Add user message locally first
        user_message = {
            'id': str(uuid.uuid4()),
            'role': 'user',
            'content': content.strip(),
            'created_at': now
        }
        session['messages'].append(user_message)

        # Call AI service
        suggested_recipes = []
        try:
            assistant_content, suggested_recipes = cls._call_ai_chat(
                session_id=session_id,
                message=content.strip(),
                user_pantry=user_pantry
            )
        except Exception as e:
            print(f" [ChatService] AI call failed: {e}")
            # Fallback response
            assistant_content = (
                "Xin lỗi, tôi đang gặp sự cố kết nối với AI service. "
                "Vui lòng thử lại sau hoặc kiểm tra xem AI service đã chạy chưa."
            )

        assistant_message = {
            'id': str(uuid.uuid4()),
            'role': 'assistant',
            'content': assistant_content,
            'suggested_recipes': suggested_recipes,
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

    @classmethod
    def _call_ai_chat(cls, session_id, message, user_pantry=None):
        """
        Call food-ai-service chat endpoint.
        Returns tuple of (assistant_content, suggested_recipes).
        """
        endpoint = f"{cls._get_ai_endpoint()}/sessions/{session_id}/messages"
        
        # Get recipes for RAG context
        recipes = cls._get_recipes_for_context()
        
        # Build request payload
        payload = {
            "message": message,
            "recipes": recipes,
            "user_pantry": user_pantry or []
        }
        
        req = urlrequest.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            method='POST',
            headers={
                'Content-Type': 'application/json'
            }
        )
        
        try:
            with urlrequest.urlopen(req, timeout=60) as response:
                raw = response.read().decode('utf-8')
                parsed = json.loads(raw)
            
            if parsed.get('success'):
                data = parsed.get('data', {})
                assistant_msg = data.get('assistant_message', {})
                content = assistant_msg.get('content', 'Không có phản hồi từ AI')
                suggested_recipes = assistant_msg.get('suggested_recipes') or data.get('suggested_recipes', [])
                return content, suggested_recipes
            else:
                raise RuntimeError(parsed.get('message', 'AI service error'))
        
        except urlerror.HTTPError as exc:
            # If session doesn't exist on AI service, create it first
            if exc.code == 404:
                cls._ensure_ai_session(session_id)
                # Retry
                with urlrequest.urlopen(req, timeout=60) as response:
                    raw = response.read().decode('utf-8')
                    parsed = json.loads(raw)
                
                if parsed.get('success'):
                    data = parsed.get('data', {})
                    assistant_msg = data.get('assistant_message', {})
                    content = assistant_msg.get('content', 'Không có phản hồi từ AI')
                    suggested_recipes = assistant_msg.get('suggested_recipes') or data.get('suggested_recipes', [])
                    return content, suggested_recipes
            
            raise RuntimeError(f'AI Service HTTP error: {exc.code}')
        except (urlerror.URLError, TimeoutError) as exc:
            raise RuntimeError(f'AI Service connection failed: {exc}')
    
    @classmethod
    def _ensure_ai_session(cls, session_id):
        """Create session on AI service if it doesn't exist"""
        endpoint = f"{cls._get_ai_endpoint()}/sessions"
        
        payload = {"title": cls._sessions.get(session_id, {}).get('title', 'Chat')}
        
        req = urlrequest.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            method='POST',
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urlrequest.urlopen(req, timeout=10) as response:
                response.read()
        except Exception:
            pass  # Ignore errors, we'll handle them in the main call

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
        if session['title'] != 'Cuộc trò chuyện mới':
            return

        for message in session['messages']:
            if message['role'] == 'user':
                truncated = message['content'][:40]
                session['title'] = truncated + ('...' if len(message['content']) > 40 else '')
                return
