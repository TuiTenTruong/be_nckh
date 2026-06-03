"""Vision API integration service - Calls food-ai-service microservice"""
import io
import json
import os
from urllib import request as urlrequest
from urllib import error as urlerror
from flask import current_app


class VisionService:
    """Service for calling food-ai-service microservice"""

    @staticmethod
    def _build_analyze_image_endpoint():
        """Build analyze-image endpoint from config/env in a backward-compatible way."""
        configured_endpoint = (
            current_app.config.get('AI_SERVICE_ENDPOINT')
            or os.getenv('AI_SERVICE_ENDPOINT')
        )
        if configured_endpoint:
            return configured_endpoint

        base_url = (
            current_app.config.get('AI_SERVICE_BASE_URL')
            or os.getenv('AI_SERVICE_BASE_URL')
            or 'http://127.0.0.1:8000'
        ).rstrip('/')

        if base_url.endswith('/api/ai'):
            return f'{base_url}/analyze-image'
        if base_url.endswith('/api/ai/analyze-image'):
            return base_url
        return f'{base_url}/api/ai/analyze-image'

    @staticmethod
    def detect_ingredients(image_bytes, filename):
        """
        Call food-ai-service /api/ai/analyze-image endpoint
        
        Args:
            image_bytes: Raw image bytes
            filename: Original filename
            
        Returns:
            tuple: (detections list, ai_suggestion dict, provider string)
        """
        endpoint = VisionService._build_analyze_image_endpoint()
        provider = 'food_ai_service'

        # Build multipart/form-data request
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        body = io.BytesIO()
        
        # Add image file part
        body.write(f'--{boundary}\r\n'.encode('utf-8'))
        body.write(f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'.encode('utf-8'))
        body.write(b'Content-Type: application/octet-stream\r\n\r\n')
        body.write(image_bytes)
        body.write(b'\r\n')
        body.write(f'--{boundary}--\r\n'.encode('utf-8'))
        
        body_bytes = body.getvalue()

        req = urlrequest.Request(
            endpoint,
            data=body_bytes,
            method='POST',
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(body_bytes))
            }
        )

        try:
            with urlrequest.urlopen(req, timeout=60) as response:
                raw = response.read().decode('utf-8')
                parsed = json.loads(raw)

            # Parse response from food-ai-service
            # Expected format: { success: true, data: { ingredients: [...], ai_suggestion: {...} } }
            if not parsed.get('success'):
                raise RuntimeError(f"AI Service error: {parsed.get('message', 'Unknown error')}")

            data = parsed.get('data', {})
            ingredients = data.get('ingredients', [])
            ai_suggestion = data.get('ai_suggestion')

            # Normalize detections format
            normalized = []
            for item in ingredients:
                if isinstance(item, str):
                    normalized.append({'name': item, 'confidence': None})
                elif isinstance(item, dict):
                    normalized.append({
                        'name': item.get('name') or item.get('label') or '',
                        'confidence': item.get('confidence')
                    })

            detections = [d for d in normalized if d.get('name')]
            
            return detections, ai_suggestion, provider

        except urlerror.HTTPError as exc:
            raise RuntimeError(f'AI Service HTTP error: {exc.code}') from exc
        except (urlerror.URLError, TimeoutError) as exc:
            raise RuntimeError(
                f'AI Service connection failed at {endpoint}: {exc}'
            ) from exc
        except ValueError as exc:
            raise RuntimeError('AI Service returned invalid JSON') from exc
