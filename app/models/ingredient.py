"""Ingredient models"""
from datetime import datetime
from app.extensions import db


class IngredientCategory(db.Model):
    """Ingredient category model"""
    __tablename__ = 'ingredient_categories'

    id = db.Column(db.String(36), primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10))  # Emoji icon
    sort_order = db.Column(db.Integer, default=0)

    # Relationships
    ingredients = db.relationship('Ingredient', backref='category', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'icon': self.icon,
            'sort_order': self.sort_order
        }

    def __repr__(self):
        return f'<IngredientCategory {self.name}>'


class Ingredient(db.Model):
    """Ingredient model"""
    __tablename__ = 'ingredients'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(10), nullable=False)  # Emoji icon
    category_id = db.Column(db.String(36), db.ForeignKey('ingredient_categories.id'), nullable=False, index=True)
    image_url = db.Column(db.Text)
    is_popular = db.Column(db.Boolean, default=False, index=True)
    aliases = db.Column(db.JSON)  # List of alternative names
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recipe_ingredients = db.relationship('RecipeIngredient', back_populates='ingredient', lazy='dynamic')
    recipes = db.relationship(
        'Recipe',
        secondary='recipe_ingredients',
        primaryjoin='Ingredient.id == RecipeIngredient.ingredient_id',
        secondaryjoin='Recipe.id == RecipeIngredient.recipe_id',
        viewonly=True,
        lazy='dynamic'
    )

    def to_dict(self, include_category=True):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'is_popular': self.is_popular,
            'aliases': self.aliases or [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_category and self.category:
            data['category'] = self.category.to_dict()
        
        return data

    def __repr__(self):
        return f'<Ingredient {self.name}>'
