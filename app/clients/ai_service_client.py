"""AI Service Client - Gọi sang AI service nội bộ qua HTTP"""
import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)


class AIServiceClient:
    """HTTP Client để gọi AI service nội bộ"""
    
    def __init__(self):
        """Initialize với config từ Flask app"""
        # Endpoint mặc định cho recipe suggestion
        # Có thể override bằng environment variable AI_RECIPE_SUGGEST_ENDPOINT
        self.base_url = current_app.config.get(
            'AI_SERVICE_BASE_URL',
            'http://localhost:8000'
        )
        self.timeout = current_app.config.get('AI_SERVICE_TIMEOUT', 30)

    def _build_recipe_suggest_endpoint(self):
        """Build endpoint linh hoạt để tránh config base_url bị trùng path."""
        base = (self.base_url or '').rstrip('/')

        # Hỗ trợ cả 3 kiểu config:
        # 1) http://host:port
        # 2) http://host:port/api/ai
        # 3) http://host:port/api/ai/recipe-suggest
        if base.endswith('/api/ai/recipe-suggest'):
            return base
        if base.endswith('/api/ai'):
            return f"{base}/recipe-suggest"
        return f"{base}/api/ai/recipe-suggest"
    
    def suggest_recipe(self, payload):
        """
        Gọi AI service để gợi ý công thức dựa trên ingredients
        
        Args:
            payload (dict): Request payload
                {
                    "user_ingredients": ["trứng", "cà chua"],
                    "recipes": [
                        {
                            "id": "...",
                            "name": "...",
                            "ingredients": [...]
                        }
                    ],
                    "preferences": {...}  # optional
                }
                
        Returns:
            dict: Response từ AI service
                {
                    "best_recipe": {
                        "id": "...",
                        "name": "...",
                        "match_score": 0.95
                    },
                    "reason": "Bạn có đủ 8/10 nguyên liệu...",
                    "missing_ingredients": ["muối", "tiêu"],
                    "substitutions": [
                        {
                            "original": "sữa tươi",
                            "replacement": "sữa đặc",
                            "reason": "..."
                        }
                    ],
                    "instructions": "Các bước làm món...",
                    "alternative_recipes": [
                        {
                            "id": "...",
                            "name": "...",
                            "match_score": 0.85
                        }
                    ]
                }
                
        Raises:
            AIServiceError: Nếu có lỗi khi gọi AI service
        """
        endpoint = self._build_recipe_suggest_endpoint()
        
        try:
            logger.info(f"Calling AI service: {endpoint}")
            logger.info(
                "Sending recipe payload to AI service: user_ingredients=%s, recipes=%s",
                len(payload.get('user_ingredients', [])) if isinstance(payload, dict) else 0,
                len(payload.get('recipes', [])) if isinstance(payload, dict) else 0
            )
            logger.debug(f"Payload: {payload}")
            
            response = requests.post(
                endpoint,
                json=payload,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            # Log response
            logger.info(f"AI service response status: {response.status_code}")
            
            # Raise exception nếu status code không phải 2xx
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"AI service response: {result}")
            
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"AI service timeout after {self.timeout}s")
            raise AIServiceError(
                "AI service không phản hồi trong thời gian cho phép",
                status_code=504
            )
        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to AI service at {endpoint}")
            raise AIServiceError(
                "Không thể kết nối tới AI service",
                status_code=503
            )
        except requests.exceptions.HTTPError as e:
            logger.error(f"AI service HTTP error: {e}")
            error_detail = "Lỗi từ AI service"
            try:
                error_json = response.json()
                error_detail = error_json.get('detail', error_detail)
            except:
                pass
            raise AIServiceError(error_detail, status_code=response.status_code)
        except Exception as e:
            logger.error(f"Unexpected error calling AI service: {e}")
            raise AIServiceError(f"Lỗi không xác định: {str(e)}")
    
    def health_check(self):
        """
        Kiểm tra AI service có hoạt động không
        
        Returns:
            dict: {
                "status": "healthy|unhealthy",
                "message": "..."
            }
        """
        endpoint = f"{self.base_url}/health"
        
        try:
            response = requests.get(endpoint, timeout=5)
            response.raise_for_status()
            return {
                "status": "healthy",
                "message": "AI service is running"
            }
        except Exception as e:
            logger.error(f"AI service health check failed: {e}")
            return {
                "status": "unhealthy",
                "message": str(e)
            }


class AIServiceError(Exception):
    """Custom exception cho AI service errors"""
    
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
    
    def to_dict(self):
        """Convert to dict for JSON response"""
        return {
            "error": "AI Service Error",
            "message": self.message,
            "status_code": self.status_code
        }
