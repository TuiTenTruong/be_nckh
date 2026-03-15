"""Vision API integration service"""
import base64
import json
import os
from urllib import request as urlrequest
from urllib import error as urlerror


class VisionService:
    """Service for external vision API calls"""

    @staticmethod
    def detect_ingredients(image_bytes, filename):
        """Call external Vision API and return detections"""
        endpoint = os.getenv('VISION_API_ENDPOINT')
        api_key = os.getenv('VISION_API_KEY')
        provider = os.getenv('VISION_API_PROVIDER', 'mock')

        if not endpoint:
            return [
                {'name': 'ca chua', 'confidence': 0.93},
                {'name': 'hanh tay', 'confidence': 0.84}
            ], 'mock'

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

        except (urlerror.HTTPError, urlerror.URLError, TimeoutError, ValueError):
            return [], provider
