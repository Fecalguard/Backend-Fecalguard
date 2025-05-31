# Gunakan image python sebagai base
FROM python:3.12.10-slim

# Set work directory
WORKDIR /app

# Salin requirements terlebih dahulu agar Docker caching bisa optimal
COPY requirements.txt .

# Install dependency
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode ke container
COPY . .

# Jalankan aplikasi dengan uvicorn
CMD ["fastapi", "run", "src/main.py"]
