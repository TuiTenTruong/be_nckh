# BE NCKH (Flask API)

Backend cung cap API cho app Flutter, gom: ingredients, recipes, pantry, scan va chat.

## 1) Yeu cau moi truong

- Python 3.10+ (khuyen nghi 3.11)
- MariaDB/MySQL (da dung schema `nckh`)
- Windows PowerShell hoac terminal bat ky

## 2) Cai dat backend

```bash
cd be_nckh
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Cau hinh bien moi truong

Tao file `.env` trong thu muc [be_nckh](be_nckh) voi noi dung mau:

```env
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

DATABASE_URL=mysql+pymysql://root:@localhost:3306/nckh

VISION_API_PROVIDER=service_demo
SERVICE_DEMO_ENDPOINT=http://127.0.0.1:5055/mock/scan
SERVICE_DEMO_API_KEY=
```

Ghi chu:
- `DATABASE_URL` can doi theo user/password MySQL tren may ban.
- De chay scan mock, de `VISION_API_PROVIDER=service_demo`.

## 4) Khoi tao du lieu DB

1. Tao database `nckh` tren MySQL/MariaDB.
2. Import schema + seed co ban tu [be_nckh/database.sql](be_nckh/database.sql).
3. (Tuy chon) bo sung recipe/ingredient moi tu file import:

```bash
# trong mysql client
source be_nckh/sql/import_recipes_from_data.sql;
source be_nckh/sql/update_recipe_images_from_source.sql;
```

## 5) Chay backend

```bash
cd be_nckh
.venv\Scripts\activate
python run.py
```

Mac dinh API chay tai: `http://127.0.0.1:5000`

## 6) Cau hinh service_demo

Du an dang dung mock scan provider theo `SERVICE_DEMO_ENDPOINT`.

Service demo local nam tai [service_demo](service_demo) va co huong dan rieng trong [service_demo/README.md](service_demo/README.md).

Neu ban can bo file service demo hoac tai bo mau service:
- Link: https://drive.google.com/drive/folders/1zOff7GIHDPl_LKxvM62cLLb2g3IJvHPT?usp=sharing

Sau khi co folder service demo, chay service:

```bash
cd service_demo
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Mac dinh service demo chay tai: `http://127.0.0.1:5055`

## 7) API nhanh de test
- API Swagger: http://localhost:5000/swagger/#/
- Health: `GET /health`
- Ingredients: `GET /api/ingredients`
- Recipes: `GET /api/recipes`
- Scan: `POST /api/scan`
