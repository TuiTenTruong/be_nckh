"""Vision API integration service"""
import base64
import json
import os
from urllib import request as urlrequest
from urllib import error as urlerror
from flask import current_app


class VisionService:
    """Service for external vision API calls"""

    @staticmethod
    def detect_ingredients(image_bytes, filename):
        """Call external vision API and return detections"""
        provider = os.getenv('VISION_API_PROVIDER') or current_app.config.get('VISION_API_PROVIDER') or 'food-ai-service'

        if provider == 'food-ai-service':
            endpoint = (
                os.getenv('VISION_API_ENDPOINT')
                or current_app.config.get('VISION_API_ENDPOINT')
                or 'http://127.0.0.1:8000/api/ai/analyze-image'
            )
        else:
            endpoint = (
                current_app.config.get('SERVICE_DEMO_ENDPOINT')
                or os.getenv('SERVICE_DEMO_ENDPOINT')
                or os.getenv('VISION_API_ENDPOINT')
            )

        api_key = os.getenv('SERVICE_DEMO_API_KEY') or os.getenv('VISION_API_KEY')

        if not endpoint:
            raise RuntimeError(f'{provider.upper()}_ENDPOINT is required')

        if provider == 'food-ai-service':
            # Multipart form-data for food-ai-service
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            body = (
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'
                f'Content-Type: image/jpeg\r\n\r\n'
            ).encode('utf-8') + image_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')

            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Authorization': f'Bearer {api_key}' if api_key else ''
            }
        else:
            # JSON format for service_demo
            payload = {
                'provider': provider,
                'filename': filename,
                'image_base64': base64.b64encode(image_bytes).decode('utf-8')
            }
            body = json.dumps(payload).encode('utf-8')
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}' if api_key else ''
            }

        req = urlrequest.Request(
            endpoint,
            data=body,
            method='POST',
            headers=headers
        )

        try:
            with urlrequest.urlopen(req, timeout=20) as response:
                raw = response.read().decode('utf-8')
                parsed = json.loads(raw)

            data = parsed.get('data') if isinstance(parsed, dict) else None
            if isinstance(data, dict):
                detections = data.get('ingredients') or data.get('predictions') or []
            else:
                detections = parsed.get('ingredients') or parsed.get('predictions') or []

            normalized = []
            for item in detections:
                if isinstance(item, str):
                    normalized.append({'name': item, 'confidence': None})
                elif isinstance(item, dict):
                    normalized.append({
                        'name': item.get('name') or item.get('label') or '',
                        'confidence': item.get('confidence')
                    })

            return [d for d in normalized if d.get('name')], provider

        except urlerror.HTTPError as exc:
            raise RuntimeError(f'{provider} HTTP error: {exc.code}') from exc
        except (urlerror.URLError, TimeoutError) as exc:
            raise RuntimeError(f'{provider} connection failed') from exc
        except ValueError as exc:
            raise RuntimeError(f'{provider} returned invalid JSON') from exc
