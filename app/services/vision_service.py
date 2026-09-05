"""Vision API integration service - Calls food-ai-service microservice"""
import json
import os

import requests
from flask import current_app


class VisionService:
    """Service for calling food-ai-service microservice"""

    @staticmethod
    def _build_analyze_image_endpoint():
        """Build analyze-image endpoint from config/env in a backward-compatible way."""
        configured_endpoint = (
            current_app.config.get('VISION_API_ENDPOINT')
            or os.getenv('VISION_API_ENDPOINT')
            or current_app.config.get('AI_SERVICE_ENDPOINT')
            or os.getenv('AI_SERVICE_ENDPOINT')
        )
        if configured_endpoint:
            return configured_endpoint

        base_url = (
            current_app.config.get('AI_SERVICE_BASE_URL')
            or os.getenv('AI_SERVICE_BASE_URL')
            or 'http://127.0.0.1:8000'
        ).rstrip('/')

        if base_url.endswith('/api/ai/analyze-image'):
            return base_url
        if base_url.endswith('/api/ai'):
            return f'{base_url}/analyze-image'
        return f'{base_url}/api/ai/analyze-image'

    @staticmethod
    def _guess_mime_type(filename):
        lower = (filename or '').lower()
        if lower.endswith('.png'):
            return 'image/png'
        if lower.endswith('.webp'):
            return 'image/webp'
        if lower.endswith('.gif'):
            return 'image/gif'
        return 'image/jpeg'

    @staticmethod
    def detect_ingredients(image_bytes, filename, preferences=None):
        """Call food-ai-service analyze-image with multipart upload."""
        endpoint = VisionService._build_analyze_image_endpoint()
        provider = os.getenv('VISION_API_PROVIDER', 'food_ai_service')
        api_key = os.getenv('SERVICE_DEMO_API_KEY') or os.getenv('VISION_API_KEY')

        if not endpoint:
            raise RuntimeError('Vision API endpoint is not configured')

        mime_type = VisionService._guess_mime_type(filename)
        files = {
            'image': (filename or 'upload.jpg', image_bytes, mime_type),
        }
        data = {}
        if preferences:
            data['recipe_chunks'] = json.dumps(preferences, ensure_ascii=False)

        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'

        timeout = int(
            current_app.config.get('AI_SERVICE_TIMEOUT')
            or os.getenv('AI_SERVICE_TIMEOUT', 60)
        )

        try:
            response = requests.post(
                endpoint,
                files=files,
                data=data,
                headers=headers,
                timeout=timeout,
            )
        except requests.exceptions.Timeout as exc:
            raise RuntimeError('Vision service timed out') from exc
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError('Vision service connection failed') from exc

        if response.status_code >= 400:
            detail = response.text.strip()[:500] or f'HTTP {response.status_code}'
            raise RuntimeError(f'Vision service HTTP error {response.status_code}: {detail}')

        try:
            parsed = response.json()
        except ValueError as exc:
            raise RuntimeError('Vision service returned invalid JSON') from exc

        # Case 1: Standard production format (/api/v1/ingredients/detect)
        if isinstance(parsed, dict) and 'detections' in parsed:
            raw_detections = parsed.get('detections', [])
            normalized = []
            for item in raw_detections:
                name = item.get('label') or item.get('label_en') or item.get('name') or ''
                if name:
                    normalized.append({
                        'name': name,
                        'confidence': item.get('confidence'),
                    })
            return normalized, None, provider

        # Case 2: Legacy format (/api/ai/analyze-image)
        if isinstance(parsed, dict) and 'success' in parsed:
            if not parsed.get('success'):
                raise RuntimeError(
                    f"AI Service error: {parsed.get('message', 'Unknown error')}"
                )
            data_block = parsed.get('data', {})
            ingredients = data_block.get('ingredients', [])
            ai_suggestion = data_block.get('ai_suggestion')
        elif isinstance(parsed, list):
            ingredients = parsed
            ai_suggestion = None
        else:
            ingredients = []
            ai_suggestion = None

        normalized = []
        for item in ingredients:
            if isinstance(item, str):
                normalized.append({'name': item, 'confidence': None})
            elif isinstance(item, dict):
                normalized.append({
                    'name': item.get('name') or item.get('label') or item.get('label_en') or '',
                    'confidence': item.get('confidence'),
                })

        detections = [d for d in normalized if d.get('name')]
        return detections, ai_suggestion, provider
