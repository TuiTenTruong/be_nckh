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
 
# AI Service (food-ai-service) config
VISION_API_PROVIDER=food_ai_service
VISION_API_ENDPOINT=http://127.0.0.1:8000/api/ai/analyze-image
AI_SERVICE_BASE_URL=http://127.0.0.1:8000
```
 
Ghi chu:
- `DATABASE_URL` can doi theo user/password MySQL tren may ban.
- `VISION_API_PROVIDER` de mac dinh la `food_ai_service` de chay cung voi AI Service nhan dang nguyen lieu.
- `AI_SERVICE_BASE_URL` la URL dung de goi cac API gợi ý cong thuc (RAG) va API chat của AI Service.
 
## 4) Khoi tao du lieu DB
 
1. Tao database `nckh` tren MySQL/MariaDB.
2. Import schema + seed co ban tu [be_nckh/database.sql](be_nckh/database.sql).
 
 
## 5) Chay backend
 
```bash
cd be_nckh
.venv\Scripts\activate
python run.py
```
 
Mac dinh API chay tai: `http://127.0.0.1:5000`
 
## 6) Cau hinh food-ai-service
 
Du an dang dung AI Service phan tich hinh anh o port `8000` su dung model YOLO + ResNet va ho tro goi goi y bang RAG nang cao (ChromaDB + vietnamese-sbert + BGE-Reranker) ket hop voi local Ollama (Gemma 2 / Qwen 2.5) hoac OpenAI.
 
Huong dan bat AI Service:
 
```bash
cd food-ai-service
python run_ai.py
```
 
Mac dinh AI service chay tai: `http://127.0.0.1:8000`
 
## 7) API nhanh de test
- API Swagger: http://localhost:5000/swagger/#/
- Health: `GET /health`
- Ingredients: `GET /api/ingredients`
- Recipes: `GET /api/recipes`
- Scan: `POST /api/scan`
