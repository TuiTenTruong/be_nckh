#!/usr/bin/env python
"""Update ingredients.icon from data/ingredient_icons.json on existing DB."""
from __future__ import annotations

import json
from pathlib import Path

from app import create_app, db
from app.models.ingredient import Ingredient

ICONS_PATH = Path(__file__).parent / "data" / "ingredient_icons.json"


def main() -> None:
    icons = json.loads(ICONS_PATH.read_text(encoding="utf-8"))
    app = create_app()
    updated = 0
    missing = []

    with app.app_context():
        for ingredient in Ingredient.query.all():
            icon = icons.get(ingredient.name.strip())
            if not icon:
                missing.append(ingredient.name)
                continue
            if ingredient.icon != icon:
                ingredient.icon = icon
                updated += 1

        db.session.commit()

    print(f"Updated {updated} ingredient icon(s).")
    if missing:
        print(f"No mapping for {len(missing)} ingredient(s): {', '.join(missing[:10])}")


if __name__ == "__main__":
    main()
