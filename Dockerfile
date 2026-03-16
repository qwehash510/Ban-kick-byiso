FROM python:3.11-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libffi-dev \
    python3-dev \
    && apt-get clean

WORKDIR /app

# Kodu kopyala
COPY . .

# Sabit sürümlerle pip yükle
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Botu başlat
CMD ["python", "main.py"]
