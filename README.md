# Getting Started

## 1️⃣ Clone the Repository
```bash
git clone https://github.com/Fecalguard/Backend-Fecalguard.git
cd Backend-Fecalguard
```

## 2️⃣ Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 3️⃣ Configure Environment Variables
```bash
cp .env.example .env
echo -e "JWT_SECRET=your-secret\nGCP_KEY=your-google-cloud-key\nMODEL_URL=your-model-url" > .env
```

## 4️⃣ Run fastapi
### Development
```bash
fastapi dev src/main.py
```

### Production
```bash
fastapi run src/main.py
```

