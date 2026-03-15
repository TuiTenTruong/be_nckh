"""Scan models"""
from datetime import datetime
from app.extensions import db


class ScanSession(db.Model):
    """Stores one ingredient scan request/response"""
    __tablename__ = 'scan_sessions'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False, index=True)
    image_name = db.Column(db.String(255), nullable=False)
    vision_provider = db.Column(db.String(50), nullable=False, default='mock')
    raw_detections = db.Column(db.JSON, nullable=False)
    matched_ingredients = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_name': self.image_name,
            'vision_provider': self.vision_provider,
            'raw_detections': self.raw_detections or [],
            'ingredients': self.matched_ingredients or [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
