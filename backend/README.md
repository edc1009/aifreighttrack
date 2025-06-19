# Logistics AI Agent Backend

這是一個基於 LangGraph 和 Google Gemini 的智能物流助手後端服務。

## 功能特點

- 🤖 基於 Google Gemini 1.5 Pro 的智能對話
- 🔍 動態網路搜索和資訊整合
- 🧠 反思推理和知識缺口分析
- 📚 自動引用搜索來源
- 🚢 專業的物流和航運領域知識

## 安裝步驟

### 1. 安裝 Python 依賴

```bash
cd backend
pip install -r requirements.txt
```

### 2. 設置環境變數

複製環境變數模板：
```bash
cp .env.example .env
```

編輯 `.env` 文件，填入以下 API 金鑰：

#### 獲取 Gemini API Key
1. 訪問 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入 Google 帳號
3. 點擊 "Create API Key"
4. 複製生成的 API Key

#### 獲取 Google Search API Key
1. 訪問 [Google Cloud Console](https://console.cloud.google.com/)
2. 創建新項目或選擇現有項目
3. 啟用 "Custom Search API"
4. 創建憑證（API Key）
5. 複製 API Key

#### 創建 Custom Search Engine
1. 訪問 [Google Custom Search](https://cse.google.com/cse/)
2. 點擊 "Add" 創建新的搜索引擎
3. 在 "Sites to search" 中輸入 `*`（搜索整個網路）
4. 創建後，複製 Search Engine ID

### 3. 啟動服務器

```bash
python start.py
```

或者直接使用 uvicorn：
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 端點

### POST /chat
智能聊天端點，包含網路搜索功能

```json
{
  "message": "什麼是貨櫃追蹤？",
  "max_iterations": 3
}
```

### POST /simple-chat
簡化聊天端點，不使用網路搜索

```json
{
  "message": "解釋一下物流的基本概念"
}
```

### GET /health
健康檢查端點

## 開發說明

### 項目結構
```
backend/
├── main.py              # FastAPI 應用主文件
├── start.py             # 啟動腳本
├── requirements.txt     # Python 依賴
├── .env.example        # 環境變數模板
├── src/
│   └── agent/
│       └── graph.py    # LangGraph Agent 邏輯
└── README.md           # 本文件
```

### 自定義 Agent

可以在 `src/agent/graph.py` 中修改 Agent 的行為：

- `LOGISTICS_SYSTEM_PROMPT`: 修改系統提示詞
- `generate_search_queries`: 調整搜索查詢生成邏輯
- `reflect_and_analyze`: 修改反思和分析邏輯

## 故障排除

### 常見問題

1. **ImportError: No module named 'langgraph'**
   - 確保已安裝所有依賴：`pip install -r requirements.txt`

2. **API Key 錯誤**
   - 檢查 `.env` 文件中的 API Key 是否正確
   - 確保 API Key 有足夠的配額

3. **搜索功能不工作**
   - 檢查 Google Search API Key 和 Custom Search Engine ID
   - 確保已啟用 Custom Search API

4. **CORS 錯誤**
   - 確保前端和後端在正確的端口運行
   - 檢查 CORS 設置

### 日誌查看

服務器會輸出詳細的日誌信息，包括：
- API 請求和響應
- 搜索查詢和結果
- 錯誤信息

## 生產部署

對於生產環境，建議：

1. 使用 Docker 容器化部署
2. 設置 Redis 和 PostgreSQL（完整 LangGraph 功能）
3. 配置反向代理（Nginx）
4. 設置 HTTPS
5. 限制 CORS 來源

## 許可證

本項目基於 MIT 許可證開源。