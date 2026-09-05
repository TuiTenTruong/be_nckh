"""Recipe Ingredient models"""
from app.extensions import db
from app.utils.ingredient_amount import format_ingredient_amount


class RecipeIngredient(db.Model):
    """Recipe ingredient model - Maps ingredients to recipes with quantity info"""
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.String(36), primary_key=True)
    recipe_id = db.Column(db.String(36), db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    ingredient_id = db.Column(db.String(36), db.ForeignKey('ingredients.id', ondelete='SET NULL'), index=True)
    quantity = db.Column(db.String(50), nullable=False, default='')
    unit = db.Column(db.String(50), nullable=False, default='')
    is_optional = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)

    # Relationships
    recipe = db.relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients')

    @property
    def display_amount(self) -> str:
        return format_ingredient_amount(self.quantity, self.unit)

    def to_dict(self, include_ingredient=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'ingredient_id': self.ingredient_id,
            'quantity': self.quantity or '',
            'unit': self.unit or '',
            'is_optional': self.is_optional,
            'sort_order': self.sort_order,
        }

        if include_ingredient and self.ingredient:
            data['ingredient'] = self.ingredient.to_dict()
            data['name'] = self.ingredient.name

        return data

    def __repr__(self):
        label = self.ingredient.name if self.ingredient else self.ingredient_id
        return f'<RecipeIngredient {label} ({self.display_amount})>'
