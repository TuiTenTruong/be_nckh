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
        """Call external service-demo API and return detections"""
        endpoint = (
            current_app.config.get('SERVICE_DEMO_ENDPOINT')
            or os.getenv('SERVICE_DEMO_ENDPOINT')
            or os.getenv('VISION_API_ENDPOINT')
        )
        api_key = os.getenv('SERVICE_DEMO_API_KEY') or os.getenv('VISION_API_KEY')
        provider = os.getenv('VISION_API_PROVIDER', 'service_demo')

        if not endpoint:
            raise RuntimeError('SERVICE_DEMO_ENDPOINT is required')

        payload = {
            'provider': provider,
            'filename': filename,
            'image_base64': base64.b64encode(image_bytes).decode('utf-8')
        }

        req = urlrequest.Request(
            endpoint,
            data=json.dumps(payload).encode('utf-8'),
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}' if api_key else ''
            }
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
            raise RuntimeError(f'Service demo HTTP error: {exc.code}') from exc
        except (urlerror.URLError, TimeoutError) as exc:
            raise RuntimeError('Service demo connection failed') from exc
        except ValueError as exc:
            raise RuntimeError('Service demo returned invalid JSON') from exc
