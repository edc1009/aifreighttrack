# Gemini Fullstack LangGraph 整合指南

本指南說明如何將 [Gemini Fullstack LangGraph](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart.git) 整合到現有的 Logistics Chat 系統中。

## 🎯 整合目標

將原本使用 OpenAI API 的簡單聊天系統升級為：
- 基於 Google Gemini 1.5 Pro 的智能對話
- 動態網路搜索和資訊整合
- 反思推理和知識缺口分析
- 專業的物流和航運領域知識
- 自動引用搜索來源

## 📁 新增的文件結構

```
BL track/
├── backend/                    # 新增：Python LangGraph 後端
│   ├── src/
│   │   └── agent/
│   │       ├── __init__.py
│   │       └── graph.py        # LangGraph Agent 邏輯
│   ├── main.py                 # FastAPI 服務器
│   ├── start.py                # 啟動腳本
│   ├── test_agent.py           # 測試腳本
│   ├── requirements.txt        # Python 依賴
│   ├── .env.example           # 環境變數模板
│   └── README.md              # 後端文檔
├── server/                     # 現有：Node.js 服務器（保持不變）
├── index.html                  # 修改：更新前端 JavaScript
├── package.json               # 修改：添加後端啟動腳本
└── INTEGRATION_GUIDE.md       # 本文件
```

## 🚀 快速開始

### 1. 安裝依賴

#### 安裝 Python 後端依賴
```bash
npm run install-backend
# 或者手動安裝
cd backend
pip install -r requirements.txt
```

#### 安裝 Node.js 依賴（如果需要）
```bash
npm install
```

### 2. 設置 API Keys

複製環境變數模板：
```bash
cp backend/.env.example backend/.env
```

編輯 `backend/.env` 文件，設置以下 API Keys：

#### 🔑 必需的 API Keys

1. **Gemini API Key**
   - 訪問：https://makersuite.google.com/app/apikey
   - 登入 Google 帳號並創建 API Key
   - 設置：`GEMINI_API_KEY=your_key_here`

2. **Google Search API Key**（可選，用於網路搜索）
   - 訪問：https://console.cloud.google.com/
   - 啟用 "Custom Search API"
   - 創建 API Key
   - 設置：`GOOGLE_API_KEY=your_key_here`

3. **Custom Search Engine ID**（可選）
   - 訪問：https://cse.google.com/cse/
   - 創建搜索引擎，搜索範圍設為 `*`
   - 設置：`GOOGLE_CSE_ID=your_cse_id_here`

### 3. 測試系統

```bash
# 測試後端功能
npm run test-backend
```

### 4. 啟動服務

#### 方式一：同時啟動前後端（推薦）
```bash
npm run dev
```

#### 方式二：分別啟動
```bash
# 終端 1：啟動 Node.js 服務器（現有功能）
npm start

# 終端 2：啟動 Python AI 後端
npm run start-backend
```

### 5. 訪問應用

- 前端應用：http://localhost:3000（或您的 Node.js 端口）
- AI 後端 API：http://localhost:8000
- API 文檔：http://localhost:8000/docs

## 🔧 系統架構

### 混合架構設計

```
前端 (HTML/JS)
    |
    ├── Tracking 功能 → Node.js Server (port 3000)
    └── AI Chat 功能 → Python FastAPI (port 8000)
                           |
                           └── LangGraph Agent
                               ├── Gemini 1.5 Pro
                               └── Google Search API
```

### 功能分工

- **Node.js Server**：處理現有的貨櫃追蹤功能
- **Python FastAPI**：處理 AI 聊天和智能搜索
- **前端**：統一界面，根據功能調用不同後端

## 🆕 新功能特點

### 1. 智能對話
- 基於 Gemini 1.5 Pro 的專業物流知識
- 支援中英文對話
- 上下文理解和記憶

### 2. 動態搜索
- 自動生成搜索關鍵詞
- 實時網路資訊查詢
- 多輪搜索優化

### 3. 反思推理
- 分析搜索結果完整性
- 識別知識缺口
- 迭代改進答案品質

### 4. 專業領域
- 貨櫃運輸和追蹤
- 國際航運和港口
- 海關和貿易法規
- 供應鏈管理

## 🔄 API 端點

### 新增的 AI 後端端點

#### POST /chat
完整的智能聊天（包含搜索）
```json
{
  "message": "最新的貨櫃運費是多少？",
  "max_iterations": 3
}
```

#### POST /simple-chat
簡化聊天（不使用搜索）
```json
{
  "message": "什麼是物流？"
}
```

#### GET /health
健康檢查

### 現有端點（保持不變）
- Node.js 服務器的所有現有 API

## 🛠️ 自定義配置

### 修改 AI 行為

編輯 `backend/src/agent/graph.py`：

```python
# 修改系統提示詞
LOGISTICS_SYSTEM_PROMPT = """
你的自定義提示詞...
"""

# 調整搜索參數
max_iterations = 3  # 最大搜索輪數
search_results_count = 5  # 每次搜索結果數量
```

### 修改前端行為

編輯 `index.html`：

```javascript
// 修改 API 地址
const AGENT_API_URL = 'http://your-backend-url:8000';

// 調整每日限制
const MAX_DAILY_CHATS = 50;
```

## 🚨 故障排除

### 常見問題

1. **Python 依賴安裝失敗**
   ```bash
   # 使用虛擬環境
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或 venv\Scripts\activate  # Windows
   pip install -r backend/requirements.txt
   ```

2. **API Key 錯誤**
   - 檢查 `.env` 文件格式
   - 確認 API Key 有效性
   - 檢查 API 配額

3. **CORS 錯誤**
   - 確認前後端端口正確
   - 檢查防火牆設置

4. **搜索功能不工作**
   - 檢查 Google Search API 設置
   - 確認 Custom Search Engine 配置
   - 可以只使用簡化聊天功能

### 測試步驟

```bash
# 1. 測試 Python 環境
python --version

# 2. 測試依賴安裝
cd backend && python -c "import langgraph; print('LangGraph OK')"

# 3. 測試 API Keys
cd backend && python test_agent.py

# 4. 測試服務器
curl http://localhost:8000/health
```

## 📈 性能優化

### 開發環境
- 使用 `reload=True` 自動重載
- 限制搜索迭代次數
- 使用簡化聊天作為備用

### 生產環境
- 設置 Redis 緩存
- 配置 PostgreSQL 持久化
- 使用 Docker 容器化
- 設置負載均衡

## 🔮 未來擴展

### 可能的改進
1. 添加語音輸入/輸出
2. 整合更多物流 API
3. 添加圖表和可視化
4. 支援多語言
5. 添加用戶認證
6. 整合企業 ERP 系統

### 進階功能
1. 智能報表生成
2. 預測性分析
3. 自動化工作流
4. 多模態輸入（圖片、文檔）

## 📞 支援

如果遇到問題：
1. 查看 `backend/README.md` 詳細文檔
2. 運行 `npm run test-backend` 診斷
3. 檢查服務器日誌
4. 參考原始項目：https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart

---

🎉 **恭喜！您已成功整合 Gemini Fullstack LangGraph 到您的物流系統中！**