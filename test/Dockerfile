# ==========================================
# 階段 1：Builder（建立隔離虛擬環境並安裝套件）
# ==========================================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ==========================================
# 階段 2：Runtime（乾淨執行環境 + Chromium + 中文字型）
# ==========================================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# 1. 從 Builder 複製虛擬環境
COPY --from=builder /opt/venv /opt/venv

# 2. 安裝 Chromium 瀏覽器、系統依賴，以及 Noto CJK 中文字型避免截圖亂碼
RUN apt-get update && \
    apt-get install -y --no-install-recommends fonts-noto-cjk && \
    playwright install --with-deps chromium && \
    rm -rf /var/lib/apt/lists/*

# 3. 複製端對端測試腳本
COPY test_e2e.py .

RUN mkdir -p /app/reports

CMD ["python", "test_e2e.py"]