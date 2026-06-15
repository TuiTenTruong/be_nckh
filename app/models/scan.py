"""Scan models"""
from datetime import datetime
from app.extensions import db


class ScanSession(db.Model):
    """Stores one ingredient scan request/response"""
    __tablename__ = 'scan_sessions'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False, index=True)
    image_name = db.Column(db.String(255), nullable=False)
    vision_provider = db.Column(db.String(50), nullable=False, default='food_ai_service')
    raw_detections = db.Column(db.JSON, nullable=False)
    matched_ingredients = db.Column(db.JSON, nullable=False)
    ai_suggestion = db.Column(db.JSON, nullable=True)  # Vision AI suggestion (legacy)
    recipe_suggestion = db.Column(db.JSON, nullable=True)  # Recipe suggestion từ RAG AI service
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        # Lấy danh sách ingredient names đã match
        matched_names = []
        for item in (self.matched_ingredients or []):
            if item.get('matched') and item.get('ingredient'):
                name = item['ingredient'].get('name')
                if name:
                    matched_names.append(name)
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_name': self.image_name,
            'vision_provider': self.vision_provider,
            'raw_detections': self.raw_detections or [],
            'ingredients': self.matched_ingredients or [],
            'matched_ingredient_names': matched_names,  # Convenience field
            'ai_suggestion': self.ai_suggestion,  # Legacy vision suggestion
            'recipe_suggestion': self.recipe_suggestion,  # Recipe suggestion từ AI
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
