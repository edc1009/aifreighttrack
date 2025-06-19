#!/usr/bin/env python3
"""
啟動 Logistics AI Agent 服務器
"""

import os
import sys
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """檢查環境變數"""
    required_vars = [
        'GEMINI_API_KEY',
        'GOOGLE_API_KEY', 
        'GOOGLE_CSE_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ 缺少必要的環境變數:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n請創建 .env 文件並設置這些變數。")
        print("參考 .env.example 文件獲取更多信息。")
        return False
    
    print("✅ 環境變數檢查通過")
    return True

def main():
    print("🚀 啟動 Logistics AI Agent...")
    
    # 載入環境變數
    from dotenv import load_dotenv
    load_dotenv()
    
    # 檢查環境
    if not check_environment():
        sys.exit(1)
    
    # 啟動服務器
    try:
        import uvicorn
        from main import app
        
        print("\n📡 服務器啟動中...")
        print("🌐 API 地址: http://localhost:8000")
        print("📚 API 文檔: http://localhost:8000/docs")
        print("\n按 Ctrl+C 停止服務器")
        print("-" * 50)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,  # 開發模式下自動重載
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 服務器已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()