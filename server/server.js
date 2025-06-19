const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();

// 啟用CORS，允許前端應用訪問
app.use(cors());

// 解析JSON請求體
app.use(express.json());

// 提供靜態文件
app.use(express.static(path.join(__dirname, '..')));

// 緩存token
let tokenCache = {
  token: null,
  expiresAt: 0
};

// 獲取token的函數
async function getToken() {
  const now = Date.now();
  if (tokenCache.token && tokenCache.expiresAt > now) {
    return tokenCache.token;
  }

  try {
    const auth = Buffer.from(
      `${process.env.EMC_CLIENT_ID}:${process.env.EMC_CLIENT_SECRET}`
    ).toString('base64');

    console.log('正在嘗試獲取token...');
    
    const response = await axios.post(
      process.env.EMC_TOKEN_URL,
      null,
      {
        headers: {
          'Authorization': `Basic ${auth}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );

    console.log('Token獲取成功');

    const token = response.data.access_token;
    const expiresIn = (response.data.expires_in || 60) - 10;
    tokenCache = {
      token,
      expiresAt: now + expiresIn * 1000
    };

    return token;
  } catch (error) {
    console.error('獲取token失敗:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    });
    throw new Error('獲取授權token失敗');
  }
}

// Token端點 - 僅用於測試
app.get('/api/token-test', async (req, res) => {
  try {
    const token = await getToken();
    res.json({ success: true, message: 'Token獲取成功' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// TNT API - 獲取事件（使用GET方法）
app.get('/api/events', async (req, res) => {
  try {
    const token = await getToken();
    
    const queryParams = req.query;
    
    const response = await axios.get(
      `${process.env.EMC_API_URL}/events`,
      {
        params: queryParams,
        headers: {
          'Authorization': `Bearer ${token}`,
          'API-Version': '2.2'
        }
      }
    );
    
    res.json(response.data);
  } catch (error) {
    console.error('API請求失敗:', error.response?.data || error.message);
    res.status(error.response?.status || 500).json({
      success: false,
      error: error.response?.data || error.message
    });
  }
});

// 集裝箱追蹤
app.get('/api/track/container/:containerNumber', async (req, res) => {
  try {
    const token = await getToken();
    const { containerNumber } = req.params;
    
    const response = await axios.get(
      `${process.env.EMC_API_URL}/events`,
      {
        params: { equipmentReference: containerNumber },
        headers: {
          'Authorization': `Bearer ${token}`,
          'API-Version': '2.2'
        }
      }
    );
    
    res.json(response.data);
  } catch (error) {
    console.error('追蹤集裝箱失敗:', error.response?.data || error.message);
    res.status(error.response?.status || 500).json({
      success: false,
      error: error.response?.data || error.message
    });
  }
});

// 提單追蹤
app.get('/api/track/bl/:blNumber', async (req, res) => {
  try {
    const token = await getToken();
    const { blNumber } = req.params;
    
    const response = await axios.get(
      `${process.env.EMC_API_URL}/events`,
      {
        params: { transportDocumentReference: blNumber },
        headers: {
          'Authorization': `Bearer ${token}`,
          'API-Version': '2.2'
        }
      }
    );
    
    res.json(response.data);
  } catch (error) {
    console.error('追蹤提單失敗:', error.response?.data || error.message);
    res.status(error.response?.status || 500).json({
      success: false,
      error: error.response?.data || error.message
    });
  }
});

// 啟動服務器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API代理服務器運行在 http://localhost:${PORT}`);
});