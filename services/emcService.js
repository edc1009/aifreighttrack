import config from '../config.js';

// 代理服務器基礎URL
const PROXY_BASE_URL = 'http://localhost:3000/api';

// 緩存token
let tokenCache = {
  token: null,
  expiresAt: 0
};

/**
 * 獲取授權token
 * @returns {Promise<string>} 授權token
 */
async function getToken() {
  try {
    // 使用代理服務器測試token是否可用
    const response = await fetch(`${PROXY_BASE_URL}/token-test`);
    const data = await response.json();
    
    if (!data.success) {
      throw new Error('Token獲取失敗');
    }
    
    return 'proxy-token'; // 實際token由代理服務器管理，前端不需要知道
  } catch (error) {
    console.error('獲取token失敗:', error);
    throw error;
  }
}

/**
 * 發送API請求
 * @param {string} endpoint - API端點
 * @param {Object} params - 請求參數
 * @returns {Promise<Object>} API響應
 */
async function makeApiRequest(endpoint, params = {}) {
  try {
    // 發送GET請求到代理服務器
    const url = `${PROXY_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      // 檢查響應的 Content-Type
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        try {
          const errorData = await response.json();
          throw new Error(errorData.error || '請求失敗');
        } catch (jsonError) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
      } else {
        // 如果不是 JSON 響應，直接使用狀態碼和狀態文本
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    }
    
    // 檢查成功響應的 Content-Type
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    } else {
      throw new Error('服務器返回了非 JSON 響應');
    }
  } catch (error) {
    console.error('API請求失敗:', error);
    throw error;
  }
}

/**
 * 追蹤集裝箱
 * @param {string} containerNumber - 集裝箱號碼
 * @returns {Promise<Object>} 追蹤結果
 */
async function trackContainer(containerNumber) {
  return await makeApiRequest(`/track/container/${containerNumber}`);
}

/**
 * 追蹤提單
 * @param {string} blNumber - 提單號碼
 * @returns {Promise<Object>} 追蹤結果
 */
async function trackBL(blNumber) {
  return await makeApiRequest(`/track/bl/${blNumber}`);
}

// 導出函數
export default {
  getToken,
  trackContainer,
  trackBL
};