from typing import TypedDict, List, Optional
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.schema import HumanMessage, SystemMessage
import os
from datetime import datetime
import json
import re

# 狀態定義
class AgentState(TypedDict):
    user_query: str
    search_queries: List[str]
    search_results: List[dict]
    all_search_results: List[dict]  # 累積所有搜索結果
    reflection: str
    knowledge_gaps: List[str]
    final_answer: str
    sources: List[str]
    iteration_count: int
    max_iterations: int
    search_summary: str  # 搜索結果摘要
    confidence_score: float  # 答案信心度

# 初始化函数
def get_llm():
    """获取LLM实例"""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )

def get_search():
    """获取搜索工具实例"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not google_api_key or not google_cse_id or google_api_key == "your_google_search_api_key_here":
        print("警告：Google搜索API未配置，将使用模拟搜索")
        return None
    
    return GoogleSearchAPIWrapper(
        google_api_key=google_api_key,
        google_cse_id=google_cse_id,
        k=5
    )

# 物流專家系統提示詞
LOGISTICS_SYSTEM_PROMPT = """
你是一位專業的物流和航運專家助手，具有以下專業領域的深度知識：

🚢 核心專業領域：
- 貨櫃運輸和即時追蹤系統
- 國際航運路線和港口操作
- 海關清關和國際貿易法規
- 供應鏈管理和優化策略
- 物流成本分析和費率比較
- 主要航運公司服務評估（Maersk, COSCO, MSC, ONE, HMM等）
- 全球港口信息和航線規劃
- 貨運保險和風險管理
- 數位化物流解決方案

💡 回答原則：
1. 提供準確、實用且可操作的建議
2. 包含具體數據、時間表、費用等詳細信息
3. 引用最新的行業資訊和法規變化
4. 提供多個解決方案選項供比較
5. 明確指出需要進一步查詢的最新資料
6. 使用專業術語但保持易懂的解釋

🎯 特別關注：
- 即時性資訊（費率、船期、港口狀況）
- 法規合規性和風險提醒
- 成本效益分析和優化建議
- 數位化工具和平台推薦
"""

def generate_search_queries(state: AgentState) -> AgentState:
    """基於用戶查詢生成搜索關鍵詞"""
    user_query = state["user_query"]
    iteration_count = state.get("iteration_count", 0)
    previous_results = state.get("all_search_results", [])
    
    # 根據迭代次數調整搜索策略
    if iteration_count == 0:
        # 第一次搜索：生成廣泛的基礎查詢
        strategy = "生成3-4個廣泛的基礎搜索詞，涵蓋問題的主要方面"
    else:
        # 後續搜索：基於已有結果生成更具體的查詢
        previous_summary = "\n".join([f"- {r.get('query', '')}: {r.get('results', '')[:200]}..." for r in previous_results[-3:]])
        strategy = f"基於已有搜索結果，生成2-3個更具體和深入的搜索詞來填補知識缺口\n\n已有結果摘要：\n{previous_summary}"
    
    prompt = f"""
    {strategy}
    
    用戶查詢：{user_query}
    
    請生成針對物流、航運、貨櫃追蹤等領域的專業搜索詞。要求：
    1. 每個搜索詞應該簡潔且具體
    2. 包含相關的專業術語和關鍵詞
    3. 考慮時效性（如"2024年"、"最新"等）
    4. 用換行符分隔，每行一個搜索詞
    
    搜索關鍵詞：
    """
    
    llm = get_llm()
    response = llm.invoke([SystemMessage(content=LOGISTICS_SYSTEM_PROMPT), HumanMessage(content=prompt)])
    search_queries = [q.strip() for q in response.content.split('\n') if q.strip() and not q.startswith('-')]
    
    # 清理和優化搜索詞
    cleaned_queries = []
    for query in search_queries[:4]:  # 限制最多4個查詢
        # 移除多餘的標點和格式
        cleaned_query = re.sub(r'^[\d\.\-\*\s]+', '', query).strip()
        if len(cleaned_query) > 5:  # 確保查詢詞有意義
            cleaned_queries.append(cleaned_query)
    
    state["search_queries"] = cleaned_queries
    return state

def web_search(state: AgentState) -> AgentState:
    """執行網路搜索"""
    search_results = []
    all_results = state.get("all_search_results", [])
    search = get_search()
    
    for query in state["search_queries"]:
        try:
            print(f"搜索查詢: {query}")
            
            if search is None:
                # 模擬搜索結果
                print("使用模擬搜索結果")
                results = f"關於 {query} 的模擬搜索結果。由於Google搜索API未配置，這是一個示例結果。"
                processed_results = results
            else:
                # 執行真實搜索
                results = search.run(query)
                # 處理和清理搜索結果
                processed_results = process_search_results(results)
            
            result_entry = {
                "query": query,
                "results": results,
                "processed_results": processed_results,
                "timestamp": datetime.now().isoformat(),
                "result_count": len(processed_results.split('\n')) if processed_results else 0
            }
            
            search_results.append(result_entry)
            all_results.append(result_entry)
            
        except Exception as e:
            print(f"搜索錯誤 '{query}': {e}")
            # 添加錯誤記錄
            error_entry = {
                "query": query,
                "results": f"搜索失敗: {str(e)}",
                "processed_results": "",
                "timestamp": datetime.now().isoformat(),
                "result_count": 0,
                "error": True
            }
            search_results.append(error_entry)
            continue
    
    state["search_results"] = search_results
    state["all_search_results"] = all_results
    return state

def process_search_results(raw_results: str) -> str:
    """處理和清理搜索結果"""
    if not raw_results:
        return ""
    
    # 移除過多的空白和重複內容
    lines = raw_results.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 10:  # 過濾太短的行
            # 移除重複的URL和無用信息
            if not any(skip_word in line.lower() for skip_word in ['cookie', 'privacy policy', 'terms of service', 'advertisement']):
                processed_lines.append(line)
    
    return '\n'.join(processed_lines[:10])  # 限制結果長度

def reflect_and_analyze(state: AgentState) -> AgentState:
    """分析搜索結果並識別知識缺口"""
    user_query = state["user_query"]
    search_results = state["search_results"]
    iteration_count = state.get("iteration_count", 0)
    all_results = state.get("all_search_results", [])
    
    # 整理當前搜索結果
    current_results_summary = ""
    successful_searches = 0
    
    for result in search_results:
        if not result.get("error", False):
            successful_searches += 1
            processed = result.get("processed_results", result.get("results", ""))
            current_results_summary += f"\n🔍 查詢: {result['query']}\n📄 結果: {processed[:300]}...\n"
    
    # 整理所有歷史結果的摘要
    all_results_summary = ""
    if len(all_results) > len(search_results):
        previous_results = all_results[:-len(search_results)]
        all_results_summary = f"\n\n📚 先前搜索摘要：\n"
        for result in previous_results[-3:]:  # 只顯示最近3個
            if not result.get("error", False):
                all_results_summary += f"- {result['query']}: {result.get('processed_results', '')[:100]}...\n"
    
    prompt = f"""
    作為物流專家，請深度分析以下搜索結果，評估是否足以回答用戶查詢。
    
    👤 用戶查詢：{user_query}
    
    🔄 當前迭代：第 {iteration_count + 1} 次搜索
    ✅ 成功搜索：{successful_searches}/{len(search_results)} 個查詢
    
    📊 當前搜索結果：{current_results_summary}
    {all_results_summary}
    
    請進行以下分析：
    
    1. **信息完整性評估** (0-100分)：
       - 是否涵蓋了用戶問題的核心要素？
       - 信息的準確性和時效性如何？
       - 是否有具體的數據、費率、時間等關鍵信息？
    
    2. **知識缺口識別**：
       - 還缺少哪些關鍵信息？
       - 哪些方面需要更深入的搜索？
       - 是否需要更具體的專業術語搜索？
    
    3. **搜索策略建議**：
       - 如果需要繼續搜索，應該關注哪些方向？
       - 建議的搜索關鍵詞類型？
    
    請按以下格式回答：
    
    **信心度分數**: [0-100]
    **評估結果**: [SUFFICIENT/NEEDS_MORE_INFO]
    **主要發現**: [簡要總結已找到的關鍵信息]
    **知識缺口**: [列出具體缺失的信息，如果沒有則寫"無"]
    **建議搜索方向**: [如果需要更多搜索，建議的方向]
    """
    
    llm = get_llm()
    response = llm.invoke([SystemMessage(content=LOGISTICS_SYSTEM_PROMPT), HumanMessage(content=prompt)])
    reflection = response.content
    
    state["reflection"] = reflection
    
    # 解析信心度分數
    confidence_match = re.search(r'信心度分數.*?[：:]\s*(\d+)', reflection)
    confidence_score = float(confidence_match.group(1)) / 100 if confidence_match else 0.5
    state["confidence_score"] = confidence_score
    
    # 檢查是否需要更多搜索
    needs_more = "NEEDS_MORE_INFO" in reflection.upper() or "需要更多" in reflection
    sufficient = "SUFFICIENT" in reflection.upper() or confidence_score >= 0.8
    
    if sufficient and not needs_more:
        state["knowledge_gaps"] = []
    else:
        # 提取知識缺口並生成新的搜索查詢
        gaps_prompt = f"""
        基於以下分析結果，生成2-3個精確的搜索查詢來填補知識缺口：
        
        分析結果：{reflection}
        
        原始用戶查詢：{user_query}
        
        請生成具體、專業的搜索關鍵詞，要求：
        1. 針對識別出的知識缺口
        2. 使用專業的物流術語
        3. 包含時效性關鍵詞（如"2024"、"最新"、"當前"）
        4. 每行一個搜索詞，不要編號或符號
        
        搜索關鍵詞：
        """
        
        llm = get_llm()
        gaps_response = llm.invoke([SystemMessage(content=LOGISTICS_SYSTEM_PROMPT), HumanMessage(content=gaps_prompt)])
        knowledge_gaps = [q.strip() for q in gaps_response.content.split('\n') if q.strip() and len(q.strip()) > 5]
        
        # 清理搜索詞
        cleaned_gaps = []
        for gap in knowledge_gaps[:3]:  # 最多3個
            cleaned_gap = re.sub(r'^[\d\.\-\*\s]+', '', gap).strip()
            if cleaned_gap and len(cleaned_gap) > 5:
                cleaned_gaps.append(cleaned_gap)
        
        state["knowledge_gaps"] = cleaned_gaps
    
    # 生成搜索結果摘要
    summary_prompt = f"""
    請為以下搜索結果生成一個簡潔的摘要（100字以內）：
    
    {current_results_summary}
    
    摘要應該突出關鍵發現和重要信息。
    """
    
    llm = get_llm()
    summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
    state["search_summary"] = summary_response.content
    
    return state

def generate_final_answer(state: AgentState) -> AgentState:
    """生成最終答案"""
    user_query = state["user_query"]
    all_search_results = state.get("all_search_results", [])
    search_summary = state.get("search_summary", "")
    confidence_score = state.get("confidence_score", 0.5)
    reflection = state.get("reflection", "")
    
    # 整理所有搜索結果，按相關性和質量排序
    relevant_results = []
    sources = []
    
    for result in all_search_results:
        if not result.get("error", False) and result.get("result_count", 0) > 0:
            processed = result.get("processed_results", result.get("results", ""))
            if processed and len(processed.strip()) > 50:  # 確保有實質內容
                relevant_results.append({
                    "query": result["query"],
                    "content": processed[:500],  # 限制長度
                    "timestamp": result.get("timestamp", "")
                })
                sources.append(result["query"])
    
    # 構建綜合的搜索結果摘要
    results_summary = "\n".join([
        f"📋 {i+1}. 搜索: {r['query']}\n   結果: {r['content'][:200]}...\n"
        for i, r in enumerate(relevant_results[:5])  # 最多5個最相關的結果
    ])
    
    prompt = f"""
    作為專業的物流和航運專家，請基於搜索結果為用戶提供全面、準確的答案。
    
    👤 **用戶查詢**: {user_query}
    
    📊 **信心度**: {confidence_score:.0%}
    📝 **搜索摘要**: {search_summary}
    
    🔍 **詳細搜索結果**:
    {results_summary}
    
    📋 **分析洞察**:
    {reflection}
    
    請提供結構化的專業回答，包含以下要素：
    
    ## 📋 核心答案
    [直接回答用戶的主要問題，要具體明確]
    
    ## 📊 關鍵信息
    [提供具體數據，如：費率、時間、規格、流程等]
    
    ## 💡 專業建議
    [基於行業經驗的實用建議和最佳實踐]
    
    ## 🔗 下一步行動
    [具體的操作步驟或聯繫方式]
    
    ## ⚠️ 注意事項
    [重要的風險提醒或合規要求]
    
    ## 📚 延伸資源
    [相關的官方網站、工具或進一步查詢建議]
    
    **回答要求**:
    - 使用專業但易懂的語言
    - 提供可操作的具體建議
    - 標註信息的時效性和可靠性
    - 如果信息不完整，明確說明限制
    - 保持客觀和準確
    """
    
    response = llm.invoke([SystemMessage(content=LOGISTICS_SYSTEM_PROMPT), HumanMessage(content=prompt)])
    
    # 後處理答案，添加信心度和免責聲明
    final_answer = response.content
    
    # 添加信心度指示
    if confidence_score < 0.7:
        confidence_note = "\n\n⚠️ **信心度提醒**: 由於搜索結果有限，部分信息可能需要進一步確認。建議聯繫相關機構獲取最新準確信息。"
        final_answer += confidence_note
    
    # 添加時效性提醒
    timestamp_note = f"\n\n🕒 **信息時效**: 以上信息基於 {datetime.now().strftime('%Y年%m月%d日')} 的搜索結果，物流行業信息變化較快，請以官方最新公告為準。"
    final_answer += timestamp_note
    
    state["final_answer"] = final_answer
    state["sources"] = sources
    
    return state

def should_continue(state: AgentState) -> str:
    """決定是否繼續搜索"""
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    knowledge_gaps = state.get("knowledge_gaps", [])
    confidence_score = state.get("confidence_score", 0.0)
    
    # 檢查是否達到最大迭代次數
    if iteration_count >= max_iterations:
        print(f"達到最大迭代次數 ({max_iterations})，生成最終答案")
        return "generate_answer"
    
    # 檢查是否沒有知識缺口
    if not knowledge_gaps:
        print("沒有發現知識缺口，生成最終答案")
        return "generate_answer"
    
    # 檢查信心度是否足夠高
    if confidence_score >= 0.85:
        print(f"信心度足夠高 ({confidence_score:.0%})，生成最終答案")
        return "generate_answer"
    
    # 檢查是否有有效的搜索結果
    all_results = state.get("all_search_results", [])
    successful_results = [r for r in all_results if not r.get("error", False) and r.get("result_count", 0) > 0]
    
    if len(successful_results) == 0 and iteration_count > 0:
        print("沒有成功的搜索結果，生成最終答案")
        return "generate_answer"
    
    print(f"繼續搜索 (第 {iteration_count + 1} 次迭代，信心度: {confidence_score:.0%})")
    return "continue_search"

def continue_search(state: AgentState) -> AgentState:
    """繼續搜索以填補知識缺口"""
    knowledge_gaps = state.get("knowledge_gaps", [])
    iteration_count = state.get("iteration_count", 0)
    
    # 更新搜索查詢為知識缺口
    state["search_queries"] = knowledge_gaps
    state["iteration_count"] = iteration_count + 1
    
    print(f"開始第 {state['iteration_count']} 次搜索，查詢: {knowledge_gaps}")
    
    return state

# 初始化狀態函數
def initialize_state(user_query: str, max_iterations: int = 3) -> AgentState:
    """初始化agent狀態"""
    return {
        "user_query": user_query,
        "search_queries": [],
        "search_results": [],
        "all_search_results": [],
        "reflection": "",
        "knowledge_gaps": [],
        "final_answer": "",
        "sources": [],
        "iteration_count": 0,
        "max_iterations": max_iterations,
        "search_summary": "",
        "confidence_score": 0.0
    }

# 構建圖
def create_logistics_agent():
    """創建物流AI agent工作流程"""
    workflow = StateGraph(AgentState)
    
    # 添加節點
    workflow.add_node("generate_queries", generate_search_queries)
    workflow.add_node("search", web_search)
    workflow.add_node("reflect", reflect_and_analyze)
    workflow.add_node("continue_search", continue_search)
    workflow.add_node("generate_answer", generate_final_answer)
    
    # 設置邊
    workflow.set_entry_point("generate_queries")
    workflow.add_edge("generate_queries", "search")
    workflow.add_edge("search", "reflect")
    
    # 條件邊：決定是否繼續搜索
    workflow.add_conditional_edges(
        "reflect",
        should_continue,
        {
            "continue_search": "continue_search",
            "generate_answer": "generate_answer"
        }
    )
    
    workflow.add_edge("continue_search", "search")
    workflow.add_edge("generate_answer", END)
    
    return workflow.compile()

# 創建agent實例
logistics_agent = create_logistics_agent()

# 便利函數：運行agent
def run_logistics_agent(user_query: str, max_iterations: int = 3) -> dict:
    """運行物流AI agent"""
    try:
        # 初始化狀態
        initial_state = initialize_state(user_query, max_iterations)
        
        # 運行工作流程
        result = logistics_agent.invoke(initial_state)
        
        return {
            "success": True,
            "answer": result.get("final_answer", "無法生成答案"),
            "sources": result.get("sources", []),
            "search_queries": [r.get("query", "") for r in result.get("all_search_results", [])],
            "confidence_score": result.get("confidence_score", 0.0),
            "iteration_count": result.get("iteration_count", 0),
            "search_summary": result.get("search_summary", "")
        }
        
    except Exception as e:
        print(f"Agent運行錯誤: {e}")
        return {
            "success": False,
            "answer": f"抱歉，處理您的請求時發生錯誤：{str(e)}",
            "sources": [],
            "search_queries": [],
            "confidence_score": 0.0,
            "iteration_count": 0,
            "search_summary": "",
            "error": str(e)
        }