# 直接使用官方預裝好 Python、Playwright 1.49.1 與 Chromium 的映像檔
FROM mcr.microsoft.com/playwright/python:v1.49.1-noble

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. 若未來有額外套件可透過 requirements.txt 安裝（playwright 本身已內建）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 補裝 Noto CJK 繁體中文字型（確保網頁截圖中文正常顯示）
RUN apt-get update && \
    apt-get install -y --no-install-recommends fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*

# 3. 複製端對端測試腳本
COPY test_e2e.py .

RUN mkdir -p /app/reports

CMD ["python", "test_e2e.py"]