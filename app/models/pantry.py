"""Pantry models"""
from datetime import datetime
from app.extensions import db


class PantryItem(db.Model):
    """Stores user pantry ingredients"""
    __tablename__ = 'pantry_items'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'ingredient_id', name='uq_pantry_user_ingredient'),
    )

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False, index=True)
    ingredient_id = db.Column(
        db.String(36),
        db.ForeignKey('ingredients.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    quantity = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    ingredient = db.relationship('Ingredient', lazy='joined')

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ingredient_id': self.ingredient_id,
            'quantity': self.quantity,
            'ingredient': self.ingredient.to_dict() if self.ingredient else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
