"""Recipe step model"""
from app.extensions import db


class RecipeStep(db.Model):
    """Recipe step model"""
    __tablename__ = 'recipe_steps'

    id = db.Column(db.String(36), primary_key=True)
    recipe_id = db.Column(db.String(36), db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    step_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer)
    tip = db.Column(db.Text)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'step_number': self.step_number,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'duration_minutes': self.duration_minutes,
            'tip': self.tip
        }

    def __repr__(self):
        return f'<RecipeStep {self.step_number}>'