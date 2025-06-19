from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.agent.graph import run_logistics_agent
import os
import json
import asyncio
from typing import AsyncGenerator
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 檢查必要的環境變數
required_env_vars = ["GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_CSE_ID"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"警告：缺少環境變數: {', '.join(missing_vars)}")
    print("請確保在 .env 文件中設置這些變數")

app = FastAPI(
    title="Logistics AI Agent", 
    version="2.0.0",
    description="增強版物流AI助手，支援串流回應和迭代搜索"
)

# CORS設置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中應該限制為特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    max_iterations: int = 3
    stream: bool = False

class ChatResponse(BaseModel):
    success: bool
    response: str
    sources: list = []
    search_queries: list = []
    confidence_score: float = 0.0
    iteration_count: int = 0
    search_summary: str = ""
    error: str = None

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """處理聊天請求 - 支援串流和非串流模式"""
    try:
        if request.stream:
            return StreamingResponse(
                stream_chat_response(request.message, request.max_iterations),
                media_type="text/plain"
            )
        else:
            # 非串流模式
            result = run_logistics_agent(request.message, request.max_iterations)
            return ChatResponse(**result)
            
    except Exception as e:
        print(f"聊天端點錯誤: {e}")
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "處理請求時發生錯誤",
                "message": str(e),
                "success": False
            }
        )

async def stream_chat_response(user_query: str, max_iterations: int = 3) -> AsyncGenerator[str, None]:
    """串流聊天回應"""
    try:
        # 發送開始訊息
        yield f"data: {json.dumps({'type': 'start', 'message': '開始處理您的請求...'}, ensure_ascii=False)}\n\n"
        
        # 模擬處理過程（實際應該與agent整合）
        yield f"data: {json.dumps({'type': 'progress', 'message': '正在搜索相關資訊...'}, ensure_ascii=False)}\n\n"
        
        # 運行agent
        result = run_logistics_agent(user_query, max_iterations)
        
        if result["success"]:
            # 發送最終結果
            yield f"data: {json.dumps({'type': 'result', 'data': result}, ensure_ascii=False)}\n\n"
        else:
            # 發送錯誤
            yield f"data: {json.dumps({'type': 'error', 'message': result.get('error', '未知錯誤')}, ensure_ascii=False)}\n\n"
        
        # 發送結束訊息
        yield f"data: {json.dumps({'type': 'end'}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': f'串流處理錯誤: {str(e)}'}, ensure_ascii=False)}\n\n"

@app.post("/simple-chat")
async def simple_chat_endpoint(request: ChatRequest):
    """簡化的聊天端點 - 與前端現有代碼兼容"""
    try:
        result = run_logistics_agent(request.message, request.max_iterations)
        
        # 返回與前端期望格式兼容的回應
        return {
            "response": result["answer"],
            "sources": result["sources"],
            "search_queries": result["search_queries"]
        }
        
    except Exception as e:
        print(f"簡化聊天端點錯誤: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"處理請求時發生錯誤: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    env_status = {
        var: "✓" if os.getenv(var) else "✗" 
        for var in required_env_vars
    }
    
    return {
        "status": "healthy", 
        "message": "Logistics AI Agent is running",
        "version": "2.0.0",
        "environment_variables": env_status,
        "features": [
            "迭代搜索",
            "知識缺口分析",
            "信心度評估",
            "串流回應",
            "來源引用"
        ]
    }

@app.get("/")
async def root():
    """根端點"""
    return {
        "message": "歡迎使用物流AI助手",
        "version": "2.0.0",
        "endpoints": {
            "/chat": "主要聊天端點（支援串流）",
            "/simple-chat": "簡化聊天端點（兼容舊版前端）",
            "/health": "健康檢查",
            "/docs": "API文檔"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"啟動物流AI助手服務器...")
    print(f"地址: http://{host}:{port}")
    print(f"API文檔: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)