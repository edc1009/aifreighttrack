# 本地設置指南 (Local Setup Guide)

## 被保留在本地的API相關文件

以下文件包含敏感的API密鑰和配置信息，已被添加到 `.gitignore` 中，不會推送到GitHub：

### API 配置文件
- `config.js` - 前端API配置（包含EMC API密鑰）
- `backend/.env` - 後端環境變量（包含Gemini API密鑰）
- `server/.env` - 服務器環境變量（包含EMC API配置）

### API 測試文件
- `test-api.js` - API測試腳本
- `test_api_connection.py` - Python API連接測試
- `test_gemini_connection.py` - Gemini API連接測試
- `test_agent.py` - Agent測試文件

### API 文檔
- `API Specification - API Developer Portal.html` - API規格文檔

## 設置步驟

### 1. 克隆倉庫後的設置

```bash
# 克隆倉庫
git clone <your-github-repo-url>
cd "BL track"
```

### 2. 創建必要的配置文件

#### 創建 `config.js`
```javascript
const config = {
    emc: {
        tokenUrl: 'https://ews.switch-hub.com/server/sol/eauth/oauth2/v1.0/token?grant_type=client_credentials&scope=TNT',
        tntApiUrl: 'https://ews.switch-hub.com/server/sol/apimg/tnt/v2',
        auth: {
            clientId: 'YOUR_CLIENT_ID',
            clientSecret: 'YOUR_CLIENT_SECRET'
        },
        apiVersion: '2.2',
        subscription: {
            enabled: false,
            callbackUrl: 'YOUR_CALLBACK_URL',
            events: ['EQUIPMENT', 'TRANSPORT', 'SHIPMENT']
        }
    }
};

Object.freeze(config);
export default config;
```

#### 創建 `backend/.env`
```env
# 獲取方式：https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Google Search API Key (可選，用於增強搜索功能)
GOOGLE_API_KEY=your_google_search_api_key_here

# Google Custom Search Engine ID (可選)
GOOGLE_CSE_ID=your_custom_search_engine_id_here

# 服務器配置
PORT=8000
HOST=0.0.0.0
DEVELOPMENT=true
```

#### 創建 `server/.env`
```env
EMC_CLIENT_SECRET=your_emc_client_secret_here
EMC_TOKEN_URL=https://ews.switch-hub.com/server/sol/eauth/oauth2/v1.0/token?grant_type=client_credentials&scope=TNT
EMC_API_URL=https://ews.switch-hub.com/server/sol/apimg/tnt/v2
```

### 3. 安裝依賴

```bash
# 安裝前端依賴
npm install

# 安裝後端依賴
cd backend
pip install -r requirements.txt
cd ..

# 安裝服務器依賴
cd server
npm install
cd ..
```

### 4. 運行應用

```bash
# 啟動前端（在項目根目錄）
python3 -m http.server 8080

# 啟動後端（在另一個終端）
cd backend
python main.py

# 啟動服務器（在另一個終端）
cd server
node server.js
```

## 安全注意事項

1. **絕對不要**將包含真實API密鑰的配置文件提交到版本控制
2. 確保 `.gitignore` 文件正確配置
3. 定期更換API密鑰
4. 在生產環境中使用環境變量而不是硬編碼的配置文件

## 故障排除

如果遇到API相關錯誤：
1. 檢查所有配置文件是否正確創建
2. 驗證API密鑰是否有效
3. 確認網絡連接正常
4. 查看控制台錯誤信息