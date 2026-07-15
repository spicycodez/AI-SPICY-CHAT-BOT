FROM python:3.11-slim

# TgCrypto ek C extension hai (Pyrogram ki fast encryption ke liye) — isko
# source se build karne ke liye gcc + python headers chahiye hote hain,
# slim image mein by default nahi hote isliye explicitly install kar rahe hain.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
