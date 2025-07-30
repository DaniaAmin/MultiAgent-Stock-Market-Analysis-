from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.team import Team
import os
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import asyncio
from collections import defaultdict

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Debug: Check if API key is loaded
if not openai_api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")
    print("Make sure your .env file contains: OPENAI_API_KEY=your-key-here")
else:
    print("API key loaded successfully")

# === Advanced Agent Definitions ===

# Web Research Agent - Enhanced with better search capabilities
web_agent = Agent(
    name="Market Research Agent",
    role="Comprehensive market research and news analysis",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[DuckDuckGoTools()],
    instructions="""
    - Search for latest market news, trends, and developments
    - Focus on credible financial sources (Reuters, Bloomberg, CNBC, etc.)
    - Analyze market sentiment and investor behavior
    - Include regulatory changes and economic indicators
    - Always cite sources with URLs
    - Provide context and implications for each finding
    """,
    show_tool_calls=True,
    markdown=True,
)

# Financial Data Agent - Enhanced with technical analysis
finance_agent = Agent(
    name="Financial Data Analyst",
    role="Comprehensive financial data analysis and technical indicators",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[YFinanceTools(
        stock_price=True, 
        analyst_recommendations=True, 
        company_info=True
    )],
    instructions="""
    - Analyze stock prices, volume, and market cap
    - Calculate and interpret technical indicators (RSI, MACD, Moving Averages)
    - Evaluate financial ratios (P/E, P/B, ROE, Debt-to-Equity)
    - Assess earnings growth and revenue trends
    - Compare with industry peers and benchmarks
    - Present data in clear tables and charts
    - Provide buy/sell/hold recommendations with reasoning
    """,
    show_tool_calls=True,
    markdown=True,
)

# Technical Analysis Agent
technical_agent = Agent(
    name="Technical Analysis Specialist",
    role="Advanced technical analysis and chart patterns",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[YFinanceTools(stock_price=True, company_info=True)],
    instructions="""
    - Identify chart patterns (head & shoulders, triangles, flags)
    - Analyze support and resistance levels
    - Calculate Fibonacci retracements and extensions
    - Assess momentum indicators (RSI, Stochastic, Williams %R)
    - Evaluate volume analysis and price action
    - Identify trend reversals and continuation patterns
    - Provide entry/exit points with risk management
    - Use candlestick patterns for short-term analysis
    """,
    show_tool_calls=True,
    markdown=True,
)

# Risk Assessment Agent
risk_agent = Agent(
    name="Risk Management Specialist",
    role="Comprehensive risk assessment and portfolio analysis",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[YFinanceTools(stock_price=True, company_info=True), DuckDuckGoTools()],
    instructions="""
    - Assess market risk and volatility
    - Analyze company-specific risks (financial, operational, regulatory)
    - Evaluate sector and industry risks
    - Calculate Value at Risk (VaR) and maximum drawdown
    - Assess correlation with broader market indices
    - Identify black swan event possibilities
    - Provide risk mitigation strategies
    - Evaluate liquidity and market depth
    - Consider geopolitical and macroeconomic risks
    """,
    show_tool_calls=True,
    markdown=True,
)

# Market Sentiment Agent
sentiment_agent = Agent(
    name="Market Sentiment Analyst",
    role="Social media sentiment and market psychology analysis",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[DuckDuckGoTools()],
    instructions="""
    - Analyze social media sentiment (Twitter, Reddit, StockTwits)
    - Monitor institutional investor sentiment
    - Track analyst rating changes and price targets
    - Assess retail vs institutional trading patterns
    - Identify market fear/greed indicators
    - Monitor options flow and short interest
    - Analyze news sentiment and media coverage
    - Track insider trading activity
    - Provide contrarian investment opportunities
    """,
    show_tool_calls=True,
    markdown=True,
)

# Portfolio Optimization Agent
portfolio_agent = Agent(
    name="Portfolio Optimization Specialist",
    role="Portfolio construction and optimization strategies",
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    tools=[YFinanceTools(stock_price=True, company_info=True)],
    instructions="""
    - Design diversified portfolio strategies
    - Calculate optimal asset allocation
    - Implement Modern Portfolio Theory principles
    - Assess correlation and diversification benefits
    - Provide sector rotation strategies
    - Design hedging strategies
    - Calculate expected returns and Sharpe ratios
    - Recommend rebalancing schedules
    - Implement dollar-cost averaging strategies
    - Provide tax-efficient investment strategies
    """,
    show_tool_calls=True,
    markdown=True,
)

# Master Coordinator Agent - Enhanced with better coordination
master_agent = Team(
    name="Financial Intelligence Hub",
    mode="coordinate",
    members=[web_agent, finance_agent, technical_agent, risk_agent, sentiment_agent, portfolio_agent],
    model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
    success_criteria="""
    A comprehensive, multi-dimensional financial analysis that includes:
    1. Market research and news analysis
    2. Financial data and technical indicators
    3. Risk assessment and management
    4. Market sentiment analysis
    5. Portfolio optimization recommendations
    6. Clear actionable insights with confidence levels
    7. Professional formatting with tables, charts, and executive summary
    """,
    instructions=[
        "Always provide executive summary at the beginning",
        "Include confidence levels for all recommendations",
        "Use professional financial terminology",
        "Provide both short-term and long-term perspectives",
        "Include risk-reward ratios for all recommendations",
        "Format data in clear tables and charts",
        "Always cite sources and provide evidence",
        "Include contrarian viewpoints when relevant",
        "Provide specific price targets and timeframes",
        "End with actionable next steps"
    ],
    show_tool_calls=True,
    markdown=True,
)

# === FastAPI Setup ===
app = FastAPI(title="Advanced Financial Analyst Multi-Agent System", version="2.0")

# Allow Streamlit to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Data Models ===
class QueryRequest(BaseModel):
    question: str
    analysis_type: Optional[str] = "comprehensive"  # comprehensive, technical, risk, sentiment, portfolio
    symbols: Optional[List[str]] = []
    timeframe: Optional[str] = "1y"  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

class PortfolioRequest(BaseModel):
    symbols: List[str]
    weights: Optional[List[float]] = None
    risk_tolerance: Optional[str] = "moderate"  # conservative, moderate, aggressive

# === In-Memory Storage for Advanced Features ===
query_history = []
portfolio_cache = {}
market_alerts = []

# === Advanced API Endpoints ===

@app.get("/")
async def root():
    return {
        "message": "Advanced Financial Analyst Multi-Agent System",
        "version": "2.0",
        "endpoints": {
            "/query": "Main analysis endpoint",
            "/portfolio": "Portfolio analysis",
            "/technical": "Technical analysis only",
            "/risk": "Risk assessment only",
            "/sentiment": "Market sentiment only",
            "/history": "Query history",
            "/alerts": "Market alerts"
        }
    }

@app.get("/test")
async def test_api_key():
    return {
        "api_key_loaded": openai_api_key is not None,
        "api_key_length": len(openai_api_key) if openai_api_key else 0,
        "agents_configured": len(master_agent.members),
        "system_status": "operational"
    }

@app.get("/simple")
async def simple_test():
    return {"message": "Advanced Financial Analyst System is operational!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_ready": len(master_agent.members),
        "api_key_configured": openai_api_key is not None
    }

@app.post("/query")
async def query_agent(request: QueryRequest):
    try:
        if not openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        # Enhanced query processing based on analysis type
        if request.analysis_type == "quick":
            enhanced_question = f"""
            Quick Analysis Request: {request.question}
            Symbols: {', '.join(request.symbols) if request.symbols else 'General market analysis'}
            Timeframe: {request.timeframe}
            
            Please provide a concise analysis including:
            1. Current stock price and basic metrics
            2. Brief market overview
            3. Key highlights and recommendations
            Keep it brief and focused on essential information.
            """
        else:
            enhanced_question = f"""
            Analysis Request: {request.question}
            Analysis Type: {request.analysis_type}
            Symbols: {', '.join(request.symbols) if request.symbols else 'General market analysis'}
            Timeframe: {request.timeframe}
            
            Please provide a comprehensive analysis including:
            1. Executive Summary
            2. Market Research & News
            3. Financial Data Analysis
            4. Technical Analysis
            5. Risk Assessment
            6. Market Sentiment
            7. Portfolio Recommendations
            8. Actionable Insights
            """
        
        print(f"Processing enhanced question: {enhanced_question}")
        
        # Run the analysis
        response = master_agent.run(enhanced_question)
        print(f"Response generated successfully")
        
        # Extract and format the content
        if hasattr(response, 'content'):
            response_str = response.content
        elif hasattr(response, '__str__'):
            response_str = str(response)
        else:
            response_str = "Response generated but could not be converted to string"
        
        # Store in history
        query_record = {
            "timestamp": datetime.now().isoformat(),
            "question": request.question,
            "analysis_type": request.analysis_type,
            "symbols": request.symbols,
            "response_length": len(response_str)
        }
        query_history.append(query_record)
        
        # Keep only last 50 queries
        if len(query_history) > 50:
            query_history.pop(0)
        
        return {
            "response": response_str,
            "metadata": {
                "analysis_type": request.analysis_type,
                "symbols_analyzed": request.symbols,
                "timeframe": request.timeframe,
                "timestamp": datetime.now().isoformat(),
                "query_id": len(query_history)
            }
        }
        
    except Exception as e:
        print(f"Error in query_agent: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/portfolio")
async def portfolio_analysis(request: PortfolioRequest):
    try:
        if not openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        portfolio_question = f"""
        Portfolio Analysis Request:
        Symbols: {', '.join(request.symbols)}
        Weights: {request.weights if request.weights else 'Equal weight'}
        Risk Tolerance: {request.risk_tolerance}
        
        Please provide:
        1. Portfolio composition analysis
        2. Risk assessment and diversification
        3. Expected returns and volatility
        4. Rebalancing recommendations
        5. Alternative portfolio suggestions
        """
        
        response = portfolio_agent.run(portfolio_question)
        
        if hasattr(response, 'content'):
            response_str = response.content
        else:
            response_str = str(response)
        
        return {"response": response_str}
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/history")
async def get_query_history():
    return {"history": query_history[-10:]}  # Return last 10 queries

@app.get("/alerts")
async def get_market_alerts():
    return {"alerts": market_alerts}

@app.post("/alerts")
async def create_market_alert(request: dict):
    alert = {
        "symbol": request.get("symbol", ""),
        "condition": request.get("condition", ""),
        "threshold": request.get("threshold", 0.0),
        "created": datetime.now().isoformat(),
        "active": True
    }
    market_alerts.append(alert)
    return {"message": "Alert created successfully", "alert": alert}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



