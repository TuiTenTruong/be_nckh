# Ingredient API Backend

Backend API cho trang Ingredient (Nguyên liệu) của ứng dụng Nhận diện Nguyên liệu & Gợi ý Công thức AI.

## Cài đặt Dependencies

```bash
pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv psycopg2-binary
```

## Cấu trúc Dự án

```
app/
├── __init__.py              # Flask app factory
├── config.py                # Configuration settings
├── extensions.py            # Extension initialization (SQLAlchemy, CORS)
├── api/
│   ├── __init__.py
│   └── ingredient_routes.py # Ingredient API endpoints
├── models/
│   ├── __init__.py
│   └── ingredient.py        # Ingredient & Category models
├── services/
│   ├── __init__.py
│   └── ingredient_service.py # Business logic
├── errors/
│   ├── __init__.py
│   └── handlers.py          # Error handlers
└── utils/
    ├── __init__.py
    └── response.py          # Response utilities
run.py                       # Entry point
.env                         # Environment variables
```

## Biến Môi Trường

Tạo file `.env`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DATABASE_URL=postgresql://user:password@localhost:5432/ingredient_db
```

## Chạy Server

```bash
python run.py
```

Server sẽ khởi chạy tại `http://localhost:5000`

## API Endpoints

### Ingredients

#### Danh sách Nguyên liệu (Phân trang + Lọc)
```
GET /api/ingredients
```

Query Parameters:
- `page` (int, default: 1): Số trang
- `per_page` (int, default: 20): Số item mỗi trang (max: 100)
- `category_id` (string): Lọc theo category ID
- `is_popular` (boolean): Lọc theo popular status
- `search` (string): Tìm kiếm theo tên hoặc aliases

Example:
```bash
curl "http://localhost:5000/api/ingredients?page=1&per_page=20&category_id=xxx&is_popular=true&search=cà chua"
```

#### Lấy Nguyên liệu theo ID
```
GET /api/ingredients/<ingredient_id>
```

#### Lấy Nguyên liệu Popular
```
GET /api/ingredients/popular?limit=10
```

#### Lấy Nguyên liệu theo Category
```
GET /api/ingredients/category/<category_id>?limit=50
```

#### Tạo Nguyên liệu Mới
```
POST /api/ingredients
Content-Type: application/json

{
  "name": "Cà chua",
  "icon": "🍅",
  "category_id": "category-uuid",
  "image_url": "https://example.com/tomato.jpg",
  "is_popular": true,
  "aliases": ["cà chua đỏ", "cà chua tươi"]
}
```

#### Cập nhật Nguyên liệu
```
PUT /api/ingredients/<ingredient_id>
Content-Type: application/json

{
  "name": "Cà chua chín",
  "is_popular": false
}
```

#### Xóa Nguyên liệu
```
DELETE /api/ingredients/<ingredient_id>
```

#### Tạo Nhiều Nguyên liệu
```
POST /api/ingredients/bulk/create
Content-Type: application/json

[
  {
    "name": "Cà chua",
    "icon": "🍅",
    "category_id": "category-uuid",
    "is_popular": true
  },
  {
    "name": "Hành tây",
    "icon": "🧅",
    "category_id": "category-uuid",
    "is_popular": true
  }
]
```

### Categories

#### Danh sách Category
```
GET /api/categories
```

#### Lấy Category theo ID
```
GET /api/categories/<category_id>
```

#### Lấy Category theo Slug
```
GET /api/categories/slug/<slug>
```

Example: `/api/categories/slug/protein`

#### Tạo Category Mới
```
POST /api/categories
Content-Type: application/json

{
  "slug": "protein",
  "name": "Chất đạm",
  "icon": "🥩",
  "sort_order": 1
}
```

#### Cập nhật Category
```
PUT /api/categories/<category_id>
Content-Type: application/json

{
  "name": "Chất đạm (Protein)",
  "sort_order": 2
}
```

#### Xóa Category
```
DELETE /api/categories/<category_id>
```

## Response Format

### Success Response
```json
{
  "success": true,
  "message": "Success message",
  "data": { ... }
}
```

### Paginated Response
```json
{
  "success": true,
  "message": "Success message",
  "data": [ ... ],
  "pagination": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "errors": null
}
```

## Database Schema

Xem file `database-schema.ts` để hiểu chi tiết về cấu trúc database.

### Bảng Chính
- `users` - Thông tin người dùng
- `ingredient_categories` - Danh mục nguyên liệu (protein, rau cu, gia vi, etc.)
- `ingredients` - Danh sách các nguyên liệu (cà chua, hành tây, etc.)
- `recipes` - Công thức nấu ăn
- `recipe_ingredients` - Nguyên liệu của các công thức (N-N mapping)
- `recipe_steps` - Các bước nấu của công thức

## Development

### Tạo Database Tables

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
```

### Seed Sample Data

```python
from app import create_app
from app.models.ingredient import IngredientCategory, Ingredient
from app.extensions import db
import uuid

app = create_app()

with app.app_context():
    # Create categories
    protein_cat = IngredientCategory(
        id=str(uuid.uuid4()),
        slug='protein',
        name='Chất đạm',
        icon='🥩',
        sort_order=1
    )
    db.session.add(protein_cat)
    db.session.commit()
    
    # Create ingredients
    ingredient = Ingredient(
        id=str(uuid.uuid4()),
        name='Cà chua',
        icon='🍅',
        category_id=protein_cat.id,
        is_popular=True,
        aliases=['cà chua đỏ', 'cà chua tươi']
    )
    db.session.add(ingredient)
    db.session.commit()
    
    print("Seed data created!")
```

## Testing

```bash
pytest
```

## Notes

- Sử dụng PostgreSQL cho production
- SQLite có thể dùng cho development/testing
- CORS được bật cho mọi routes đã đăng ký
- Tất cả timestamps lưu ở format ISO 8601
