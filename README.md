```markdown
# ⚡ NewEra — FastAPI asosidagi birinchi loyiha

## 🇺🇿 O'zbekcha

### 📝 Loyiha Tavsifi

**NewEra** — bu mening **FastAPI** framework'da yaratgan **birinchi backend loyiham**. Loyiha orqali **modern Python web API** yaratishni o‘rgandim.

> Bu loyiha orqali men REST API, `.env` konfiguratsiya fayllari, marshrutlar bilan ishlash va asinxron funksiyalar haqida dastlabki tajribalarni oldim.

---

### ⚙️ Texnologiyalar

- **Python 3.10+**
- **FastAPI**
- **Uvicorn** (development server)
- **Pydantic** (ma'lumotlar validatsiyasi uchun)
- **dotenv** (`.env` fayllar bilan ishlash uchun)

---

### 📁 Loyihaning Tuzilishi

```

NewEra/
├── app/               # Asosiy ilova fayllari (routers, models, config)
│   └── **init**.py
│   └── main.py        # FastAPI app yaratish joyi
├── .env               # Muhit o‘zgaruvchilari (port, db, tokenlar)
├── .gitignore         # Git orqali e'tiborga olinmaydigan fayllar
├── requirements.txt   # Kutubxonalar ro'yxati

````

---

### 🚀 Ishga Tushirish

1. Repozitoriyani yuklab oling:
```bash
git clone https://github.com/Abdurahmon17/NewEra.git
cd NewEra
````

2. Virtual muhit yaratib faollashtiring:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Kutubxonalarni o‘rnating:

```bash
pip install -r requirements.txt
```

4. Serverni ishga tushiring:

```bash
uvicorn app.main:app --reload
```

5. Brauzer orqali oching:

```
http://127.0.0.1:8000
```

📘 Swagger hujjati: `http://127.0.0.1:8000/docs`
📙 Redoc hujjati: `http://127.0.0.1:8000/redoc`

---

## 🇬🇧 English

### 📝 Project Description

**NewEra** is my **first backend project using FastAPI** — a modern Python web framework for building high-performance APIs.

> Through this project, I learned how to build APIs with FastAPI, use `.env` files for configuration, define async endpoints, and validate data with Pydantic.

---

### ⚙️ Technologies

* **Python 3.10+**
* **FastAPI**
* **Uvicorn**
* **Pydantic**
* **python-dotenv**

---

### 📁 Project Structure

```
NewEra/
├── app/               # Main app folder (routes, config)
│   └── __init__.py
│   └── main.py
├── .env               # Environment variables
├── .gitignore         # Ignored files
├── requirements.txt   # Dependencies
```

---

### 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/Abdurahmon17/NewEra.git
cd NewEra
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Run the development server:

```bash
uvicorn app.main:app --reload
```

5. Open in browser:

```
http://127.0.0.1:8000
```

📘 Swagger Docs: `http://127.0.0.1:8000/docs`
📙 Redoc Docs: `http://127.0.0.1:8000/redoc`

---

## 👨‍💻 Muallif / Author

**Abdurahmon Abdumavlonov**
📧 Email: [abdumavlonovabdurahmon75@gmail.com](mailto:abdumavlonovabdurahmon75@gmail.com)
🔗 GitHub: [Abdurahmon17](https://github.com/Abdurahmon17)

---

✅ Bu loyiha orqali men FastAPI asoslarini, endpointlar yaratishni, hujjat sahifalarini ko‘rishni va backend logikani modullashtirishni o‘rgandim.

```

---

✅ Bu `README.md` faylni `NewEra/README.md` fayli sifatida joylashtir.

Xohlasang `.md` formatda yuklab ham beraman.

Keyingisi — `kindergarden_org` loyihami yoki boshqa biror backend loyihangga yozaylikmi?
```
