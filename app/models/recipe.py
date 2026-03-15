"""Recipe models"""
from datetime import datetime
from app.extensions import db


class Recipe(db.Model):
    """Recipe model"""
    __tablename__ = 'recipes'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    cook_time_minutes = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, index=True)  # 'De', 'Trung binh', 'Kho'
    servings = db.Column(db.Integer, default=2, nullable=False)
    cuisine_type = db.Column(db.String(50))  # e.g., 'Viet Nam', 'Han Quoc'
    diet_tags = db.Column(db.JSON)  # e.g., ['chay', 'it dau mo']
    is_featured = db.Column(db.Boolean, default=False, index=True)
    total_favorites = db.Column(db.Integer, default=0)
    total_views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipe_ingredients = db.relationship(
        'RecipeIngredient',
        back_populates='recipe',
        lazy='dynamic',
        cascade='all, delete-orphan',
        order_by='RecipeIngredient.sort_order'
    )
    ingredients = db.relationship(
        'Ingredient',
        secondary='recipe_ingredients',
        primaryjoin='Recipe.id == RecipeIngredient.recipe_id',
        secondaryjoin='Ingredient.id == RecipeIngredient.ingredient_id',
        viewonly=True,
        lazy='dynamic'
    )
    steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_ingredients=False, include_steps=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'cook_time_minutes': self.cook_time_minutes,
            'difficulty': self.difficulty,
            'servings': self.servings,
            'cuisine_type': self.cuisine_type,
            'diet_tags': self.diet_tags or [],
            'is_featured': self.is_featured,
            'total_favorites': self.total_favorites,
            'total_views': self.total_views,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_ingredients:
            data['ingredients'] = [ri.to_dict(include_ingredient=True) for ri in self.recipe_ingredients]

        if include_steps:
            data['steps'] = [step.to_dict() for step in self.steps]

        return data

    def __repr__(self):
        return f'<Recipe {self.name}>'