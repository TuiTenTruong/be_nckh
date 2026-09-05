"""
=================================================================
AI SERVICE CONTRACT v1.0
=================================================================
Định nghĩa HTTP contract giữa BE service và AI service

Endpoint: POST /api/ai/recipe-suggest
Description: Gợi ý công thức nấu ăn dựa trên nguyên liệu người dùng có

Author: Auto-generated
=================================================================
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from enum import Enum


# =================================================================
# ENUMS
# =================================================================

class DifficultyLevel(str, Enum):
    """Độ khó của công thức"""
    EASY = "De"
    MEDIUM = "Trung binh"
    HARD = "Kho"


class ErrorCode(str, Enum):
    """Mã lỗi chuẩn hóa"""
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    EMPTY_RECIPES = "EMPTY_RECIPES"
    EMPTY_INGREDIENTS = "EMPTY_INGREDIENTS"
    OPENAI_TIMEOUT = "OPENAI_TIMEOUT"
    OPENAI_ERROR = "OPENAI_ERROR"
    NO_MATCHING_RECIPE = "NO_MATCHING_RECIPE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMITED = "RATE_LIMITED"


# =================================================================
# REQUEST SCHEMAS (BE → AI Service)
# =================================================================

class IngredientItem(BaseModel):
    """Schema cho một ingredient trong recipe"""
    name: str = Field(..., description="Tên nguyên liệu", min_length=1, max_length=100)
    quantity: str = Field(..., description="Số lượng", max_length=50)
    unit: str = Field(default="", description="Đơn vị", max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Trứng gà",
                "quantity": "3",
                "unit": "quả",
            }
        }


class RecipeItem(BaseModel):
    """Schema cho một recipe gửi sang AI service"""
    id: str = Field(..., description="Recipe ID (UUID)", min_length=1)
    name: str = Field(..., description="Tên món ăn", min_length=1, max_length=200)
    description: str = Field(..., description="Mô tả ngắn về món ăn", max_length=1000)
    steps: str = Field(..., description="Các bước nấu (đã format thành string)")
    ingredients: List[IngredientItem] = Field(..., description="Danh sách nguyên liệu")
    
    # Optional metadata
    cook_time_minutes: Optional[int] = Field(None, ge=1, le=480, description="Thời gian nấu (phút)")
    difficulty: Optional[str] = Field(None, description="Độ khó: De|Trung binh|Kho")
    cuisine_type: Optional[str] = Field(None, max_length=50, description="Loại ẩm thực")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Trứng chiên cà chua",
                "description": "Món ăn đơn giản, nhanh gọn với trứng và cà chua",
                "steps": "1. Đập trứng vào bát, đánh tan\n2. Cắt cà chua múi cau\n3. Chiên trứng...",
                "ingredients": [
                    {"name": "Trứng gà", "quantity": "3", "unit": "quả"},
                    {"name": "Cà chua", "quantity": "2", "unit": "quả"}
                ],
                "cook_time_minutes": 15,
                "difficulty": "De",
                "cuisine_type": "Viet Nam"
            }
        }


class UserPreferences(BaseModel):
    """User preferences để filter/rank recipes (OPTIONAL)"""
    difficulty: Optional[str] = Field(None, description="Độ khó mong muốn")
    cook_time_max: Optional[int] = Field(None, ge=1, le=480, description="Thời gian nấu tối đa (phút)")
    cuisine_type: Optional[str] = Field(None, description="Loại ẩm thực ưa thích")
    diet_tags: Optional[List[str]] = Field(None, description="Tags chế độ ăn: chay, it dau mo, ...")
    exclude_ingredients: Optional[List[str]] = Field(None, description="Nguyên liệu cần tránh (dị ứng)")

    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "De",
                "cook_time_max": 30,
                "cuisine_type": "Viet Nam",
                "diet_tags": ["it dau mo"],
                "exclude_ingredients": ["đậu phộng"]
            }
        }


class RecipeSuggestionRequest(BaseModel):
    """
    REQUEST SCHEMA: BE → AI Service
    
    Payload chính để yêu cầu AI gợi ý công thức
    """
    # REQUIRED fields
    user_ingredients: List[str] = Field(
        ..., 
        min_length=1,
        description="Danh sách nguyên liệu người dùng hiện có"
    )
    recipes: List[RecipeItem] = Field(
        ..., 
        min_length=1,
        description="Danh sách recipes từ database để AI chọn"
    )
    
    # OPTIONAL fields
    preferences: Optional[UserPreferences] = Field(
        None, 
        description="User preferences để ranking"
    )
    max_suggestions: Optional[int] = Field(
        3, 
        ge=1, 
        le=10, 
        description="Số lượng alternative recipes trả về"
    )
    include_substitutions: Optional[bool] = Field(
        True, 
        description="Có gợi ý thay thế nguyên liệu không"
    )
    language: Optional[str] = Field(
        "vi", 
        description="Ngôn ngữ response: vi|en"
    )
    request_id: Optional[str] = Field(
        None, 
        description="Request ID để tracing/debugging"
    )

    @field_validator('user_ingredients')
    @classmethod
    def validate_ingredients(cls, v):
        if not v:
            raise ValueError("user_ingredients không được rỗng")
        # Clean và validate từng item
        cleaned = [ing.strip() for ing in v if ing and ing.strip()]
        if not cleaned:
            raise ValueError("user_ingredients phải có ít nhất 1 nguyên liệu hợp lệ")
        return cleaned

    class Config:
        json_schema_extra = {
            "example": {
                "user_ingredients": ["trứng gà", "cà chua", "hành lá", "dầu ăn", "muối"],
                "recipes": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "name": "Trứng chiên cà chua",
                        "description": "Món ăn đơn giản",
                        "steps": "1. Đập trứng...",
                        "ingredients": [
                            {"name": "Trứng gà", "quantity": "3", "unit": "quả"},
                            {"name": "Cà chua", "quantity": "2", "unit": "quả"}
                        ],
                        "cook_time_minutes": 15,
                        "difficulty": "De"
                    }
                ],
                "preferences": {
                    "difficulty": "De",
                    "cook_time_max": 30
                },
                "max_suggestions": 3,
                "include_substitutions": True,
                "language": "vi"
            }
        }


# =================================================================
# RESPONSE SCHEMAS (AI Service → BE)
# =================================================================

class MatchedRecipe(BaseModel):
    """Recipe đã được AI chọn với score"""
    id: str = Field(..., description="Recipe ID")
    name: str = Field(..., description="Tên món ăn")
    match_score: float = Field(..., ge=0, le=1, description="Điểm khớp (0-1)")
    matched_ingredients: List[str] = Field(default_factory=list, description="Nguyên liệu đã khớp")
    matched_count: int = Field(0, ge=0, description="Số nguyên liệu khớp")
    total_ingredients: int = Field(0, ge=0, description="Tổng số nguyên liệu cần")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "Trứng chiên cà chua",
                "match_score": 0.85,
                "matched_ingredients": ["trứng gà", "cà chua", "hành lá"],
                "matched_count": 3,
                "total_ingredients": 5
            }
        }


class Substitution(BaseModel):
    """Gợi ý thay thế nguyên liệu"""
    original: str = Field(..., description="Nguyên liệu gốc cần thay")
    replacement: str = Field(..., description="Nguyên liệu thay thế")
    reason: str = Field(..., description="Lý do có thể thay thế")

    class Config:
        json_schema_extra = {
            "example": {
                "original": "Sữa tươi",
                "replacement": "Sữa đặc pha loãng",
                "reason": "Có thể thay thế với tỉ lệ 1:1, vị hơi ngọt hơn"
            }
        }


class RecipeSuggestionResponse(BaseModel):
    """
    RESPONSE SCHEMA: AI Service → BE
    
    Response thành công từ AI service
    """
    # REQUIRED fields
    success: bool = Field(True, description="Trạng thái xử lý")
    best_recipe: Optional[MatchedRecipe] = Field(None, description="Recipe phù hợp nhất")
    
    # Context & reasoning
    reason: str = Field(..., description="Lý do AI chọn recipe này")
    instructions: str = Field("", description="Hướng dẫn nấu ăn tùy chỉnh từ AI")
    
    # Ingredient analysis
    missing_ingredients: List[str] = Field(default_factory=list, description="Nguyên liệu còn thiếu")
    substitutions: List[Substitution] = Field(default_factory=list, description="Gợi ý thay thế")
    
    # Alternatives
    alternative_recipes: List[MatchedRecipe] = Field(default_factory=list, description="Các recipe thay thế")
    
    # Metadata
    request_id: Optional[str] = Field(None, description="Request ID để tracing")
    processing_time_ms: Optional[int] = Field(None, ge=0, description="Thời gian xử lý (ms)")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "best_recipe": {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "Trứng chiên cà chua",
                    "match_score": 0.85,
                    "matched_ingredients": ["trứng gà", "cà chua", "hành lá"],
                    "matched_count": 3,
                    "total_ingredients": 5
                },
                "reason": "Bạn có 3/5 nguyên liệu cần thiết.",
                "instructions": "Với nguyên liệu bạn có, hãy làm như sau...",
                "missing_ingredients": ["nước mắm", "đường"],
                "substitutions": [
                    {
                        "original": "Nước mắm",
                        "replacement": "Muối + chút nước",
                        "reason": "Có thể thay thế để tạo vị mặn tương tự"
                    }
                ],
                "alternative_recipes": [],
                "request_id": "req-abc123",
                "processing_time_ms": 1250
            }
        }


# =================================================================
# ERROR RESPONSE SCHEMA
# =================================================================

class ErrorDetail(BaseModel):
    """Chi tiết lỗi"""
    field: Optional[str] = Field(None, description="Field gây lỗi (nếu validation)")
    message: str = Field(..., description="Mô tả lỗi")


class ErrorResponse(BaseModel):
    """
    ERROR RESPONSE SCHEMA
    
    Schema chuẩn cho tất cả các lỗi từ AI service
    """
    success: bool = Field(False, description="Luôn là False cho error response")
    error_code: ErrorCode = Field(..., description="Mã lỗi chuẩn hóa")
    message: str = Field(..., description="Mô tả lỗi cho user")
    details: Optional[List[ErrorDetail]] = Field(None, description="Chi tiết lỗi (validation)")
    request_id: Optional[str] = Field(None, description="Request ID để debug")
    retry_after: Optional[int] = Field(None, description="Số giây đợi trước khi retry (rate limit)")

    class Config:
        json_schema_extra = {
            "examples": {
                "invalid_payload": {
                    "value": {
                        "success": False,
                        "error_code": "INVALID_PAYLOAD",
                        "message": "Request payload không hợp lệ",
                        "details": [
                            {"field": "user_ingredients", "message": "Không được để trống"}
                        ],
                        "request_id": "req-abc123"
                    }
                },
                "openai_timeout": {
                    "value": {
                        "success": False,
                        "error_code": "OPENAI_TIMEOUT",
                        "message": "OpenAI không phản hồi trong thời gian cho phép",
                        "request_id": "req-abc123"
                    }
                }
            }
        }


# =================================================================
# HTTP STATUS CODES MAPPING
# =================================================================

HTTP_STATUS_CODES = {
    # Success
    200: "OK - Request thành công",
    
    # Client Errors
    400: "Bad Request - Payload không hợp lệ",
    422: "Unprocessable Entity - Validation error",
    429: "Too Many Requests - Rate limited",
    
    # Server Errors
    500: "Internal Server Error - Lỗi xử lý nội bộ",
    502: "Bad Gateway - Lỗi từ OpenAI API",
    503: "Service Unavailable - AI service không khả dụng",
    504: "Gateway Timeout - OpenAI timeout",
}

ERROR_CODE_TO_STATUS = {
    ErrorCode.INVALID_PAYLOAD: 400,
    ErrorCode.EMPTY_RECIPES: 400,
    ErrorCode.EMPTY_INGREDIENTS: 400,
    ErrorCode.OPENAI_TIMEOUT: 504,
    ErrorCode.OPENAI_ERROR: 502,
    ErrorCode.NO_MATCHING_RECIPE: 200,  # Vẫn success, chỉ không có kết quả
    ErrorCode.INTERNAL_ERROR: 500,
    ErrorCode.RATE_LIMITED: 429,
}


# =================================================================
# HELPER FUNCTIONS
# =================================================================

def create_error_response(
    error_code: ErrorCode,
    message: str,
    details: Optional[List[dict]] = None,
    request_id: Optional[str] = None,
    retry_after: Optional[int] = None
) -> dict:
    """Helper để tạo error response chuẩn"""
    response = {
        "success": False,
        "error_code": error_code.value,
        "message": message,
        "request_id": request_id
    }
    if details:
        response["details"] = details
    if retry_after:
        response["retry_after"] = retry_after
    return response


def get_status_code_for_error(error_code: ErrorCode) -> int:
    """Lấy HTTP status code tương ứng với error code"""
    return ERROR_CODE_TO_STATUS.get(error_code, 500)


# =================================================================
# FULL REQUEST/RESPONSE EXAMPLES
# =================================================================

EXAMPLE_REQUEST_FULL = {
    "user_ingredients": [
        "trứng gà",
        "cà chua", 
        "hành lá",
        "dầu ăn",
        "muối",
        "tiêu"
    ],
    "recipes": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "name": "Trứng chiên cà chua",
            "description": "Món ăn đơn giản với trứng và cà chua, thích hợp cho bữa sáng hoặc bữa phụ",
            "steps": "1. Đập trứng vào bát, thêm chút muối và đánh tan\n2. Rửa sạch cà chua, cắt múi cau\n3. Phi thơm hành với dầu ăn\n4. Đổ trứng vào chiên sơ\n5. Thêm cà chua, đảo đều\n6. Nêm nếm và tắt bếp",
            "ingredients": [
                {"name": "Trứng gà", "quantity": "3", "unit": "quả"},
                {"name": "Cà chua", "quantity": "2", "unit": "quả"},
                {"name": "Hành lá", "quantity": "2", "unit": "cọng"},
                {"name": "Dầu ăn", "quantity": "2", "unit": "thìa"},
                {"name": "Nước mắm", "quantity": "1", "unit": "thìa"}
            ],
            "cook_time_minutes": 15,
            "difficulty": "De",
            "cuisine_type": "Viet Nam"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "name": "Canh cà chua trứng",
            "description": "Canh thanh mát với cà chua và trứng, dễ nấu",
            "steps": "1. Đun sôi nước\n2. Cho cà chua vào nấu mềm\n3. Đập trứng vào khuấy\n4. Nêm gia vị",
            "ingredients": [
                {"name": "Trứng gà", "quantity": "2", "unit": "quả"},
                {"name": "Cà chua", "quantity": "3", "unit": "quả"},
                {"name": "Hành lá", "quantity": "1", "unit": "cọng"},
                {"name": "Nước mắm", "quantity": "2", "unit": "thìa"}
            ],
            "cook_time_minutes": 20,
            "difficulty": "De",
            "cuisine_type": "Viet Nam"
        }
    ],
    "preferences": {
        "difficulty": "De",
        "cook_time_max": 30,
        "cuisine_type": "Viet Nam"
    },
    "max_suggestions": 3,
    "include_substitutions": True,
    "language": "vi",
    "request_id": "req-be-20240401-001"
}


EXAMPLE_RESPONSE_SUCCESS = {
    "success": True,
    "best_recipe": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Trứng chiên cà chua",
        "match_score": 0.90,
        "matched_ingredients": ["trứng gà", "cà chua", "hành lá", "dầu ăn"],
        "matched_count": 4,
        "total_ingredients": 5
    },
    "reason": "Bạn có 4/5 nguyên liệu cần thiết cho món Trứng chiên cà chua. Đây là món đơn giản, nhanh gọn (15 phút) và phù hợp với sở thích ẩm thực Việt Nam của bạn. Chỉ thiếu nước mắm nhưng có thể thay thế bằng muối.",
    "instructions": "Với nguyên liệu bạn có, hãy làm như sau:\n\n1. Đập 3 quả trứng vào bát, thêm chút muối và tiêu, đánh tan\n2. Rửa sạch 2 quả cà chua, cắt múi cau\n3. Phi thơm hành lá với 2 thìa dầu ăn\n4. Đổ trứng vào chiên sơ đến khi hơi đông\n5. Thêm cà chua vào, đảo đều\n6. Thay vì nước mắm, dùng muối để nêm nếm\n7. Rắc thêm tiêu và tắt bếp\n\nMẹo: Chiên trứng lửa vừa để không bị cháy!",
    "missing_ingredients": ["nước mắm"],
    "substitutions": [
        {
            "original": "Nước mắm",
            "replacement": "Muối",
            "reason": "Bạn đã có muối, có thể thay thế nước mắm. Dùng 1/2 thìa muối thay cho 1 thìa nước mắm."
        }
    ],
    "alternative_recipes": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "name": "Canh cà chua trứng",
            "match_score": 0.75,
            "matched_ingredients": ["trứng gà", "cà chua", "hành lá"],
            "matched_count": 3,
            "total_ingredients": 4
        }
    ],
    "request_id": "req-be-20240401-001",
    "processing_time_ms": 1523
}


EXAMPLE_RESPONSE_NO_MATCH = {
    "success": True,
    "best_recipe": None,
    "reason": "Không tìm thấy công thức phù hợp với nguyên liệu bạn có. Vui lòng thử thêm nguyên liệu hoặc điều chỉnh preferences.",
    "instructions": "",
    "missing_ingredients": [],
    "substitutions": [],
    "alternative_recipes": [],
    "request_id": "req-be-20240401-002",
    "processing_time_ms": 856
}


EXAMPLE_ERROR_INVALID_PAYLOAD = {
    "success": False,
    "error_code": "INVALID_PAYLOAD",
    "message": "Request payload không hợp lệ",
    "details": [
        {"field": "user_ingredients", "message": "Field bắt buộc, không được để trống"},
        {"field": "recipes[0].name", "message": "Tên món ăn không được vượt quá 200 ký tự"}
    ],
    "request_id": "req-be-20240401-003"
}


EXAMPLE_ERROR_EMPTY_RECIPES = {
    "success": False,
    "error_code": "EMPTY_RECIPES",
    "message": "Danh sách recipes không được rỗng",
    "details": [
        {"field": "recipes", "message": "Phải có ít nhất 1 recipe"}
    ],
    "request_id": "req-be-20240401-003"
}


EXAMPLE_ERROR_OPENAI_TIMEOUT = {
    "success": False,
    "error_code": "OPENAI_TIMEOUT",
    "message": "OpenAI không phản hồi trong thời gian cho phép (30s). Vui lòng thử lại sau.",
    "details": None,
    "request_id": "req-be-20240401-004"
}


EXAMPLE_ERROR_OPENAI_ERROR = {
    "success": False,
    "error_code": "OPENAI_ERROR",
    "message": "Lỗi từ OpenAI API: Rate limit exceeded",
    "details": None,
    "request_id": "req-be-20240401-004"
}


EXAMPLE_ERROR_RATE_LIMITED = {
    "success": False,
    "error_code": "RATE_LIMITED",
    "message": "Quá nhiều request. Vui lòng thử lại sau.",
    "details": None,
    "request_id": "req-be-20240401-005",
    "retry_after": 60
}
