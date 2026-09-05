#!/usr/bin/env python
"""
Migrate database from legacy Cookpad seed data to data_book.json schema.

- Resets recipe-related tables and re-seeds from data_book.json
- Adds/normalizes columns: recipes.source, recipe_ingredients.quantity, recipe_ingredients.unit (drops legacy amount)
- Keeps operational tables: pantry_items, scan_sessions (cleared demo rows)
- Optionally exports database.sql dump after migration
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

from sqlalchemy import inspect, text

from app import create_app, db
from app.models.ingredient import Ingredient, IngredientCategory
from app.models.recipe import Recipe
from app.models.recipeIngredient import RecipeIngredient
from app.models.recipeStep import RecipeStep

DATA_BOOK_PATH = Path(__file__).parent / "app" / "schemas" / "ingredient_task" / "data_book.json"
INGREDIENT_ICONS_PATH = Path(__file__).parent / "data" / "ingredient_icons.json"
SQL_DUMP_PATH = Path(__file__).parent / "database.sql"
BACKUP_DIR = Path(__file__).parent / "backups"

CATEGORY_DEFS = {
    "c1": {"slug": "thit-ca", "name": "Thịt cá", "icon": "🍗", "sort_order": 1},
    "c2": {"slug": "trung-sua", "name": "Trứng sữa", "icon": "🥚", "sort_order": 2},
    "c3": {"slug": "rau-cu", "name": "Rau củ", "icon": "🥬", "sort_order": 3},
    "c4": {"slug": "tinh-bot", "name": "Tinh bột", "icon": "🍚", "sort_order": 4},
    "c5": {"slug": "gia-vi", "name": "Gia vị", "icon": "🧂", "sort_order": 5},
}

CATEGORY_ICONS = {cid: info["icon"] for cid, info in CATEGORY_DEFS.items()}


def load_ingredient_icons() -> dict[str, str]:
    if not INGREDIENT_ICONS_PATH.exists():
        return {}
    return json.loads(INGREDIENT_ICONS_PATH.read_text(encoding="utf-8"))


def icon_for_ingredient(name: str, category_id: str) -> str:
    icons = load_ingredient_icons()
    return icons.get(name.strip(), CATEGORY_ICONS.get(category_id, "🥘"))


def slugify(name: str) -> str:
    normalized = unicodedata.normalize("NFD", name.lower())
    ascii_text = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    return ascii_text.strip("_") or "item"


def ensure_schema_columns():
    """Normalize schema: quantity + unit only (no redundant amount)."""
    inspector = inspect(db.engine)
    recipe_cols = {c["name"] for c in inspector.get_columns("recipes")}
    ri_cols = {c["name"] for c in inspector.get_columns("recipe_ingredients")}

    if "source" not in recipe_cols:
        db.session.execute(text("ALTER TABLE recipes ADD COLUMN source TEXT NULL"))
        print("  + Added recipes.source")

    if "quantity" not in ri_cols:
        db.session.execute(
            text("ALTER TABLE recipe_ingredients ADD COLUMN quantity VARCHAR(50) NOT NULL DEFAULT ''")
        )
        print("  + Added recipe_ingredients.quantity")
        ri_cols.add("quantity")

    if "unit" not in ri_cols:
        db.session.execute(
            text("ALTER TABLE recipe_ingredients ADD COLUMN unit VARCHAR(50) NOT NULL DEFAULT ''")
        )
        print("  + Added recipe_ingredients.unit")
        ri_cols.add("unit")

    if "amount" in ri_cols:
        db.session.execute(
            text(
                "UPDATE recipe_ingredients SET quantity = TRIM(SUBSTRING_INDEX(amount, ' ', 1)), "
                "unit = TRIM(SUBSTRING(amount, LOCATE(' ', amount))) "
                "WHERE (quantity IS NULL OR quantity = '') AND amount IS NOT NULL AND amount != ''"
            )
        )
        db.session.execute(text("ALTER TABLE recipe_ingredients DROP COLUMN amount"))
        print("  ✓ Dropped legacy recipe_ingredients.amount")

    db.session.commit()


def reset_recipe_data():
    """Remove legacy recipe/ingredient data. Keep table structure."""
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for table in (
        "recipe_steps",
        "recipe_ingredients",
        "recipes",
        "pantry_items",
        "scan_sessions",
        "ingredients",
    ):
        db.session.execute(text(f"TRUNCATE TABLE `{table}`"))
        print(f"  ✓ Truncated {table}")
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    db.session.commit()


def seed_categories():
    for cid, info in CATEGORY_DEFS.items():
        existing = IngredientCategory.query.get(cid)
        if existing:
            existing.slug = info["slug"]
            existing.name = info["name"]
            existing.icon = info["icon"]
            existing.sort_order = info["sort_order"]
        else:
            db.session.add(
                IngredientCategory(
                    id=cid,
                    slug=info["slug"],
                    name=info["name"],
                    icon=info["icon"],
                    sort_order=info["sort_order"],
                )
            )
    db.session.commit()


def load_data_book() -> list[dict]:
    with open(DATA_BOOK_PATH, encoding="utf-8") as f:
        return json.load(f)


def _safe_int(value, default: int = 30) -> int:
    if value is None or value == "":
        return default
    return int(value)


def seed_from_data_book(recipes_data: list[dict]) -> dict:
    ingredient_cache: dict[str, Ingredient] = {}
    ing_counter = 0
    stats = {
        "recipes": 0,
        "ingredients": 0,
        "recipe_ingredients": 0,
        "recipe_steps": 0,
    }

    for idx, item in enumerate(recipes_data, 1):
        recipe_id = f"recipe-book-{idx:04d}"
        recipe = Recipe(
            id=recipe_id,
            name=item["name"],
            description=item.get("description", ""),
            image_url=item.get("image_url", ""),
            cook_time_minutes=_safe_int(item.get("cook_time_minutes"), 30),
            difficulty=item.get("difficulty") or "medium",
            servings=_safe_int(item.get("servings"), 2),
            cuisine_type=item.get("cuisine_type", "Vietnamese"),
            diet_tags=item.get("diet_tags") or [],
            source=item.get("source"),
            is_featured=False,
            total_favorites=0,
            total_views=0,
        )
        db.session.add(recipe)
        stats["recipes"] += 1

        for sort_idx, ing_data in enumerate(item.get("ingredients", []), 1):
            ing_name = ing_data["name"].strip()
            category_id = ing_data.get("category_id", "c5")

            if ing_name not in ingredient_cache:
                ing_counter += 1
                ing_id = f"ing-book-{ing_counter:04d}"
                ingredient = Ingredient(
                    id=ing_id,
                    name=ing_name,
                    icon=icon_for_ingredient(ing_name, category_id),
                    category_id=category_id,
                    image_url=f"images/{slugify(ing_name)}.jpg",
                    is_popular=False,
                    aliases=[],
                )
                db.session.add(ingredient)
                ingredient_cache[ing_name] = ingredient
                stats["ingredients"] += 1

            quantity = str(ing_data.get("quantity", "")).strip()
            unit = str(ing_data.get("unit", "")).strip()
            db.session.add(
                RecipeIngredient(
                    id=f"rig-book-{idx:04d}-{sort_idx:02d}",
                    recipe_id=recipe_id,
                    ingredient_id=ingredient_cache[ing_name].id,
                    quantity=quantity,
                    unit=unit,
                    is_optional=bool(ing_data.get("is_optional", False)),
                    sort_order=sort_idx,
                )
            )
            stats["recipe_ingredients"] += 1

        for step in item.get("instructions", []):
            db.session.add(
                RecipeStep(
                    id=f"rst-book-{idx:04d}-{int(step['step_number']):02d}",
                    recipe_id=recipe_id,
                    step_number=int(step["step_number"]),
                    title=step.get("title"),
                    description=step.get("description", ""),
                    image_url=None,
                    duration_minutes=None,
                    tip=step.get("tip"),
                )
            )
            stats["recipe_steps"] += 1

        if idx % 20 == 0:
            db.session.commit()
            print(f"  … processed {idx}/{len(recipes_data)} recipes")

    db.session.commit()
    return stats


def find_mysqldump() -> str | None:
    candidates = [
        r"C:\xampp\mysql\bin\mysqldump.exe",
        r"C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysqldump.exe",
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
        r"C:\Program Files\MariaDB 10.4\bin\mysqldump.exe",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def export_sql_dump(database_url: str | None = None) -> Path | None:
    """Export nckh database to database.sql via mysqldump."""
    from urllib.parse import urlparse

    url = database_url or os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/nckh")
    parsed = urlparse(url)
    db_name = parsed.path.lstrip("/")
    auth, host_port = parsed.netloc.split("@") if "@" in parsed.netloc else ("", parsed.netloc)
    user, password = auth.split(":", 1) if ":" in auth else (auth, "")
    host, port = host_port.split(":") if ":" in host_port else (host_port, "3306")

    mysqldump = find_mysqldump()
    if not mysqldump:
        print("  ⚠ mysqldump not found — skip SQL export (install XAMPP/Laragon or add to PATH)")
        return None

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"nckh_{timestamp}.sql"

    cmd = [
        mysqldump,
        f"-h{host}",
        f"-P{port}",
        f"-u{user}",
        "--single-transaction",
        "--routines",
        "--triggers",
        "--default-character-set=utf8mb4",
        db_name,
    ]
    env = os.environ.copy()
    if password:
        env["MYSQL_PWD"] = password

    with open(SQL_DUMP_PATH, "w", encoding="utf-8") as out, open(backup_path, "w", encoding="utf-8") as backup:
        result = subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, env=env, check=False)
        if result.returncode != 0:
            print(f"  ✗ mysqldump failed: {result.stderr.decode('utf-8', errors='replace')}")
            return None
        subprocess.run(cmd, stdout=backup, stderr=subprocess.PIPE, env=env, check=True)

    print(f"  ✓ Exported {SQL_DUMP_PATH}")
    print(f"  ✓ Backup copy: {backup_path}")
    return SQL_DUMP_PATH


def migrate(export: bool = True) -> dict:
    print("=" * 60)
    print(" DATABASE MIGRATION: data_book.json → MySQL (nckh)")
    print("=" * 60)

    recipes_data = load_data_book()
    print(f"\n📚 Loaded {len(recipes_data)} recipes from data_book.json")

    print("\n🔧 Ensuring schema columns…")
    ensure_schema_columns()

    print("\n🗑️  Clearing legacy recipe/ingredient data…")
    reset_recipe_data()

    print("\n🏷️  Seeding ingredient categories (c1–c5)…")
    seed_categories()

    print("\n📥 Seeding recipes, ingredients, steps…")
    stats = seed_from_data_book(recipes_data)

    print("\n✅ Migration complete:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")

    if export:
        print("\n💾 Exporting SQL dump…")
        export_sql_dump()

    return stats


def main():
    parser = argparse.ArgumentParser(description="Migrate nckh DB from data_book.json")
    parser.add_argument("--no-export", action="store_true", help="Skip mysqldump export")
    args = parser.parse_args()

    app = create_app(os.getenv("FLASK_ENV", "development"))
    with app.app_context():
        migrate(export=not args.no_export)


if __name__ == "__main__":
    main()
