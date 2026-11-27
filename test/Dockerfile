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
# 階段 2：Runtime（使用官方預裝好瀏覽器與依賴的 Playwright 映像檔）
# ==========================================
FROM mcr.microsoft.com/playwright/python:v1.49.1-noble AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# 1. 從 Builder 複製 Python 虛擬環境
COPY --from=builder /opt/venv /opt/venv

# 2. 補裝 Noto CJK 繁體中文字型（確保網頁截圖中文正常顯示）
RUN apt-get update && \
    apt-get install -y --no-install-recommends fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*

# 3. 複製端對端測試腳本
COPY test_e2e.py .

RUN mkdir -p /app/reports

CMD ["python", "test_e2e.py"]