FROM python:3.11

RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libffi-dev \
    python3-dev \
    git \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
