# 🚀 Fullstack Expense Manager & Playwright E2E Docker Architecture

這是一個結合 **全端 CRUD 應用（Nginx + FastAPI + PostgreSQL）** 與 **端對端自動化驗證（Playwright E2E）** 的多容器微服務架構專案。透過單一 `docker-compose.yml` 編排四個獨立容器，實現「一鍵啟動環境 ➔ 反向代理無跨域通訊 ➔ 資料庫持久化 ➔ 自動化瀏覽器驗證並匯出截圖報告」的完整工程閉環。

---

## 🏗️ 系統架構與容器分工

| 容器服務 | 技術選型 | 核心職責 | 網路與 Port 配置 |
| :--- | :--- | :--- | :--- |
| **`db`** | `postgres:16-alpine` | 儲存消費紀錄資料，搭配 Named Volume 持久化 | 僅內部網路 `5432`（不對外暴露） |
| **`api`** | `Python FastAPI` | 提供完整 `GET / POST / PUT / DELETE` RESTful API | 內部 `8000` / 本機映射 `8030` |
| **`web`** | `Nginx` + HTML/JS | 託管前端 SPA 介面，並將 `/api/` 反向代理轉發至後端 | 對外映射本機 **`8080:80`** |
| **`e2e-tester`** | `Playwright` (Multi-stage) | **測試專職容器**（`test` profile），自動執行全端 CRUD 驗證與截圖 | 執行完畢自動銷毀並匯出至 `./reports` |

---

## 📁 專案結構

```text
fullstack-e2e-docker/
├── backend/                 # FastAPI 後端服務
│   ├── Dockerfile
│   ├── main.py              # 支援 GET / POST / PUT / DELETE 與 SQLAlchemy 模型
│   └── requirements.txt
├── frontend/                # Nginx 反向代理與前端網頁
│   ├── Dockerfile
│   ├── nginx.conf           # 靜態頁面託管 + /api/ 反向代理轉發設定
│   └── index.html           # 單頁式操作介面（支援行內編輯與即時統計）
├── e2e/                     # Playwright 自動化驗證容器
│   ├── Dockerfile           # Multi-stage Build + Noto CJK 中文字型支援
│   ├── requirements.txt
│   └── test_e2e.py          # 端對端 CRUD 測試與自動截圖腳本
├── reports/                 # 自動匯出的 E2E 測試截圖（.png）與報告（.json）
├── .env                     # 資料庫環境變數設定（未設定時自動套用 Compose 預設值）
├── .gitignore               # 排除敏感設定與測試產物
├── docker-compose.yml       # 核心 4 容器服務編排檔
└── README.md                # 專案說明與維運指南
```

---

## 🚀 快速啟動與執行測試

### 1. 啟動全端應用服務（DB + API + Web）

```bash
docker compose up -d --build
```

* **前端消費記帳介面**：`http://localhost:8080`
* **後端 Swagger API 文件**：`http://localhost:8030/docs`

---

### 2. 執行 Playwright 端對端自動化驗證（E2E Testing）

確保上述全端服務啟動後，執行以下指令派出無頭瀏覽器機器人自動測試完整 CRUD 流程：

```bash
docker compose --profile test run --rm --build e2e-tester
```

**自動化驗證涵蓋步驟：**
1. **GET 載入驗證**：透過內部 DNS 連入 `http://web` 驗證頁面標題與結構。
2. **POST 新增驗證**：自動填寫項目名稱、金額（`$3500`）與分類並送出。
3. **PUT 與持久化驗證**：切換行內編輯將金額改為 `$3200`，並執行 `page.reload()` 驗證資料確實寫入 PostgreSQL。
4. **DELETE 清理驗證**：點擊刪除並確認該列資料從 DOM 中移除。
5. **證據匯出**：所有步驟皆自動截圖並生成 JSON 報告存放於本機 `./reports/` 目錄。

---

## 🛠️ Docker Compose 常用維運指令

### 1. 狀態檢查與日誌監控
* **查看所有運行中容器與健康檢查狀態：**
  ```bash
  docker compose ps
  ```
* **即時監看後端 API 與資料庫日誌：**
  ```bash
  docker compose logs -f api db
  ```

### 2. 進入容器與資料庫除錯
* **進入 PostgreSQL 資料庫檢查實際儲存資料：**
  ```bash
  docker compose exec db psql -U admin -d expense_db -c "SELECT * FROM expense_items;"
  ```
* **進入前端 Nginx 容器檢查反向代理設定：**
  ```bash
  docker compose exec web sh
  ```

### 3. 停止與環境清理
* **停止並移除容器與內部網路（保留資料庫 Volume）：**
  ```bash
  docker compose down
  ```
* **徹底停止並移除容器、網路與所有資料庫 Volume：**
  ```bash
  docker compose down -v
  ```