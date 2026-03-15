"""Recipe Ingredient models"""
from app.extensions import db


class RecipeIngredient(db.Model):
    """Recipe ingredient model - Maps ingredients to recipes with quantity info"""
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.String(36), primary_key=True)
    recipe_id = db.Column(db.String(36), db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    ingredient_id = db.Column(db.String(36), db.ForeignKey('ingredients.id', ondelete='SET NULL'), index=True)
    amount = db.Column(db.String(50), nullable=False)
    is_optional = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    # Relationships
    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')

    def to_dict(self, include_ingredient=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'ingredient_id': self.ingredient_id,
            'amount': self.amount,
            'is_optional': self.is_optional,
            'sort_order': self.sort_order
        }

        if include_ingredient and self.ingredient:
            data['ingredient'] = self.ingredient.to_dict()

        return data

    def __repr__(self):
        return f'<RecipeIngredient {self.ingredient.name} ({self.amount})>'
