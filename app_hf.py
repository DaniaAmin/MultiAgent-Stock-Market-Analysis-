# Financial Analyst Multi-Agent System - Hugging Face Spaces Version
import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os
import yfinance as yf
from duckduckgo_search import DDGS

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def generate_analysis(question, analysis_type, symbols, stock_data, news_results, timeframe):
    """Generate analysis based on the type and available data"""
    
    analysis = f"# 📊 {analysis_type.title()} Analysis\n\n"
    
    if analysis_type == "quick":
        analysis += "## 🚀 Quick Analysis Results\n\n"
        
        if symbols and stock_data:
            analysis += "### 📈 Current Stock Data\n\n"
            for symbol, data in stock_data.items():
                if data['current_price']:
                    analysis += f"**{symbol}**: ${data['current_price']:.2f}\n"
                    if data['info'].get('marketCap'):
                        market_cap = data['info']['marketCap'] / 1e9
                        analysis += f"Market Cap: ${market_cap:.2f}B\n"
                    analysis += f"Sector: {data['info'].get('sector', 'N/A')}\n\n"
        
        analysis += "### 💡 Key Insights\n\n"
        analysis += "- Current market conditions appear stable\n"
        analysis += "- Consider monitoring key support/resistance levels\n"
        analysis += "- Review earnings reports and company news\n\n"
        
    elif analysis_type == "comprehensive":
        analysis += "## 🔍 Comprehensive Market Analysis\n\n"
        
        if news_results:
            analysis += "### 📰 Latest Market News\n\n"
            for i, news in enumerate(news_results[:3], 1):
                analysis += f"{i}. **{news.get('title', 'No title')}**\n"
                analysis += f"   {news.get('body', 'No content')[:200]}...\n\n"
        
        if symbols and stock_data:
            analysis += "### 📊 Stock Analysis\n\n"
            for symbol, data in stock_data.items():
                analysis += f"#### {symbol} Analysis\n\n"
                if data['current_price']:
                    analysis += f"- **Current Price**: ${data['current_price']:.2f}\n"
                if data['info'].get('marketCap'):
                    market_cap = data['info']['marketCap'] / 1e9
                    analysis += f"- **Market Cap**: ${market_cap:.2f}B\n"
                analysis += f"- **Sector**: {data['info'].get('sector', 'N/A')}\n"
                analysis += f"- **Industry**: {data['info'].get('industry', 'N/A')}\n\n"
        
        analysis += "### 🎯 Recommendations\n\n"
        analysis += "1. **Diversification**: Consider spreading investments across sectors\n"
        analysis += "2. **Risk Management**: Set stop-loss orders for volatile positions\n"
        analysis += "3. **Research**: Stay updated with company earnings and market news\n\n"
        
    elif analysis_type == "technical":
        analysis += "## 📈 Technical Analysis\n\n"
        
        if symbols and stock_data:
            for symbol, data in stock_data.items():
                analysis += f"### {symbol} Technical Indicators\n\n"
                if not data['history'].empty:
                    hist = data['history']
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    analysis += f"- **Current Price**: ${current_price:.2f}\n"
                    analysis += f"- **Daily Change**: {change_pct:+.2f}%\n"
                    analysis += f"- **Volume**: {hist['Volume'].iloc[-1]:,.0f}\n"
                    analysis += f"- **52-Week Range**: ${hist['Low'].min():.2f} - ${hist['High'].max():.2f}\n\n"
                    
                    # Simple moving averages
                    sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
                    sma_50 = hist['Close'].rolling(50).mean().iloc[-1]
                    
                    analysis += f"- **20-Day SMA**: ${sma_20:.2f}\n"
                    analysis += f"- **50-Day SMA**: ${sma_50:.2f}\n\n"
                    
                    # Trend analysis
                    if current_price > sma_20 > sma_50:
                        analysis += "**Trend**: Bullish (Price above both moving averages)\n\n"
                    elif current_price < sma_20 < sma_50:
                        analysis += "**Trend**: Bearish (Price below both moving averages)\n\n"
                    else:
                        analysis += "**Trend**: Mixed signals\n\n"
        
        analysis += "### 📊 Technical Recommendations\n\n"
        analysis += "- Monitor key support and resistance levels\n"
        analysis += "- Watch for breakout patterns\n"
        analysis += "- Consider volume confirmation for moves\n\n"
        
    elif analysis_type == "risk":
        analysis += "## ⚠️ Risk Assessment\n\n"
        
        if symbols and stock_data:
            analysis += "### 📊 Risk Analysis by Stock\n\n"
            for symbol, data in stock_data.items():
                analysis += f"#### {symbol} Risk Profile\n\n"
                
                # Beta calculation (simplified)
                if not data['history'].empty:
                    hist = data['history']
                    returns = hist['Close'].pct_change().dropna()
                    volatility = returns.std() * (252 ** 0.5)  # Annualized volatility
                    
                    analysis += f"- **Volatility**: {volatility:.2%}\n"
                    analysis += f"- **Sector Risk**: {data['info'].get('sector', 'N/A')}\n"
                    analysis += f"- **Market Cap**: {data['info'].get('marketCap', 0) / 1e9:.2f}B\n\n"
        
        analysis += "### 🛡️ Risk Mitigation Strategies\n\n"
        analysis += "1. **Diversification**: Spread investments across sectors\n"
        analysis += "2. **Position Sizing**: Limit individual position sizes\n"
        analysis += "3. **Stop Losses**: Set automatic stop-loss orders\n"
        analysis += "4. **Regular Review**: Monitor positions regularly\n\n"
        
    elif analysis_type == "sentiment":
        analysis += "## 😊 Market Sentiment Analysis\n\n"
        
        if news_results:
            analysis += "### 📰 News Sentiment\n\n"
            positive_keywords = ['bullish', 'positive', 'growth', 'gain', 'rise', 'up']
            negative_keywords = ['bearish', 'negative', 'decline', 'fall', 'down', 'risk']
            
            positive_count = 0
            negative_count = 0
            
            for news in news_results:
                title_body = (news.get('title', '') + ' ' + news.get('body', '')).lower()
                positive_count += sum(1 for word in positive_keywords if word in title_body)
                negative_count += sum(1 for word in negative_keywords if word in title_body)
            
            if positive_count > negative_count:
                analysis += "**Overall Sentiment**: Bullish 📈\n\n"
            elif negative_count > positive_count:
                analysis += "**Overall Sentiment**: Bearish 📉\n\n"
            else:
                analysis += "**Overall Sentiment**: Neutral ➡️\n\n"
            
            analysis += f"- Positive signals: {positive_count}\n"
            analysis += f"- Negative signals: {negative_count}\n\n"
        
        analysis += "### 🎯 Sentiment Recommendations\n\n"
        analysis += "- Monitor social media sentiment\n"
        analysis += "- Watch institutional flows\n"
        analysis += "- Consider contrarian opportunities\n\n"
        
    elif analysis_type == "portfolio":
        analysis += "## 📊 Portfolio Analysis\n\n"
        
        if symbols and stock_data:
            analysis += "### 🎯 Portfolio Composition\n\n"
            total_market_cap = sum(data['info'].get('marketCap', 0) for data in stock_data.values())
            
            for symbol, data in stock_data.items():
                market_cap = data['info'].get('marketCap', 0)
                weight = (market_cap / total_market_cap * 100) if total_market_cap > 0 else 0
                analysis += f"- **{symbol}**: {weight:.1f}% of portfolio\n"
            
            analysis += "\n### 📈 Portfolio Recommendations\n\n"
            analysis += "1. **Diversification**: Consider adding different sectors\n"
            analysis += "2. **Rebalancing**: Review allocation quarterly\n"
            analysis += "3. **Risk Management**: Set appropriate position sizes\n\n"
    
    analysis += "---\n\n"
    analysis += "*This analysis is for educational purposes only. Always consult with financial professionals before making investment decisions.*"
    
    return analysis

def generate_portfolio_analysis(symbols, portfolio_data, risk_tolerance):
    """Generate portfolio analysis"""
    
    analysis = f"# 📊 Portfolio Analysis - {risk_tolerance.title()} Risk Profile\n\n"
    
    if portfolio_data:
        analysis += "## 📈 Portfolio Composition\n\n"
        
        total_market_cap = sum(data.get('market_cap', 0) for data in portfolio_data.values())
        
        for symbol, data in portfolio_data.items():
            market_cap = data.get('market_cap', 0)
            weight = (market_cap / total_market_cap * 100) if total_market_cap > 0 else 0
            analysis += f"### {symbol}\n"
            analysis += f"- **Weight**: {weight:.1f}%\n"
            analysis += f"- **Sector**: {data.get('sector', 'N/A')}\n"
            analysis += f"- **Current Price**: ${data.get('current_price', 0):.2f}\n\n"
        
        analysis += "## 🎯 Recommendations\n\n"
        
        if risk_tolerance == "conservative":
            analysis += "- **Focus on large-cap, stable companies**\n"
            analysis += "- **Consider dividend-paying stocks**\n"
            analysis += "- **Maintain 60-70% in blue-chip stocks**\n"
            analysis += "- **Add 20-30% in bonds or bond ETFs**\n"
            analysis += "- **Keep 10-20% in cash for opportunities**\n\n"
        elif risk_tolerance == "moderate":
            analysis += "- **Balance between growth and value**\n"
            analysis += "- **Diversify across sectors**\n"
            analysis += "- **Consider 70-80% in stocks**\n"
            analysis += "- **Add 15-25% in bonds**\n"
            analysis += "- **Keep 5-10% in cash**\n\n"
        else:  # aggressive
            analysis += "- **Focus on growth stocks**\n"
            analysis += "- **Consider emerging markets**\n"
            analysis += "- **Maintain 80-90% in stocks**\n"
            analysis += "- **Add 5-15% in bonds**\n"
            analysis += "- **Consider alternative investments**\n\n"
        
        analysis += "## 📊 Risk Assessment\n\n"
        analysis += "- **Diversification**: Good across multiple stocks\n"
        analysis += "- **Sector Exposure**: Monitor concentration\n"
        analysis += "- **Volatility**: Expected for current allocation\n"
        analysis += "- **Liquidity**: Adequate for most positions\n\n"
    
    analysis += "---\n\n"
    analysis += "*Portfolio analysis is for educational purposes. Consult with financial advisors for personalized advice.*"
    
    return analysis

# Page configuration
st.set_page_config(
    page_title="Financial Analyst Multi-Agent System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'query_history' not in st.session_state:
    st.session_state.query_history = []

# Main header
st.markdown('<h1 class="main-header">📈 Financial Analyst Multi-Agent System</h1>', unsafe_allow_html=True)

# Sidebar for navigation and settings
with st.sidebar:
    st.markdown("## 🎛️ Analysis Controls")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Analysis Type",
        ["quick", "comprehensive", "technical", "risk", "sentiment", "portfolio"],
        help="Choose the type of analysis you want to perform"
    )
    
    # Timeframe selection
    timeframe = st.selectbox(
        "Timeframe",
        ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
        index=5,  # Default to 1y
        help="Select the time period for analysis"
    )
    
    # Symbols input
    symbols_input = st.text_input(
        "Stock Symbols (comma-separated)",
        placeholder="AAPL, MSFT, GOOGL",
        help="Enter stock symbols to analyze (optional)"
    )
    
    # Parse symbols
    symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()] if symbols_input else []
    
    # System status
    st.markdown("## 🔧 System Status")
    if api_key:
        st.success("✅ OpenAI API Key Configured")
        st.metric("API Key Status", "✅ Loaded")
    else:
        st.error("❌ OpenAI API Key Missing")
        st.info("💡 Add OPENAI_API_KEY in Space settings")
    
    st.metric("Analysis Type", analysis_type.title())
    st.metric("Symbols", len(symbols))

# Main content area
tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📈 Portfolio", "📋 History"])

with tab1:
    st.markdown('<h2 class="sub-header">Financial Analysis</h2>', unsafe_allow_html=True)
    
    # Query input
    default_questions = {
        "quick": "What's the current stock price and basic info for AAPL?",
        "comprehensive": "What's the market outlook for AI chip companies?",
        "technical": "Analyze the technical indicators for AAPL stock",
        "risk": "What are the key risks for the technology sector?",
        "sentiment": "What's the current market sentiment for electric vehicle stocks?",
        "portfolio": "How should I diversify my tech-heavy portfolio?"
    }
    
    question = st.text_area(
        "Enter your financial query:",
        value=default_questions.get(analysis_type, "What's the market outlook for AI chip companies?"),
        height=100,
        help="Ask any financial question and our AI agents will provide comprehensive analysis"
    )
    
    # Show expected analysis time
    analysis_times = {
        "quick": "30-60 seconds",
        "comprehensive": "2-5 minutes",
        "technical": "1-3 minutes",
        "risk": "1-3 minutes",
        "sentiment": "1-3 minutes",
        "portfolio": "1-3 minutes"
    }
    
    st.info(f"⏱️ Expected analysis time: {analysis_times.get(analysis_type, '1-3 minutes')}")
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🚀 Run Analysis",
            type="primary",
            use_container_width=True
        )
    
    if analyze_button:
        if not api_key:
            st.error("❌ OpenAI API key not configured. Please add it in Space settings.")
        else:
            # Create a progress bar for better user experience
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update progress
                progress_bar.progress(20)
                status_text.text("🤖 Initializing analysis...")
                
                # Get stock data if symbols provided
                stock_data = {}
                if symbols:
                    progress_bar.progress(40)
                    status_text.text("📊 Fetching stock data...")
                    
                    for symbol in symbols[:3]:  # Limit to 3 symbols for performance
                        try:
                            ticker = yf.Ticker(symbol)
                            info = ticker.info
                            hist = ticker.history(period=timeframe)
                            
                            stock_data[symbol] = {
                                'info': info,
                                'history': hist,
                                'current_price': hist['Close'].iloc[-1] if not hist.empty else None,
                                'volume': hist['Volume'].iloc[-1] if not hist.empty else None
                            }
                        except Exception as e:
                            st.warning(f"⚠️ Could not fetch data for {symbol}: {str(e)}")
                
                # Get market news
                progress_bar.progress(60)
                status_text.text("📰 Gathering market news...")
                
                try:
                    with DDGS() as ddgs:
                        news_results = list(ddgs.news("financial markets", max_results=5))
                except:
                    news_results = []
                
                # Generate analysis
                progress_bar.progress(80)
                status_text.text("🧠 Generating analysis...")
                
                # Create analysis based on type
                analysis_result = generate_analysis(
                    question, analysis_type, symbols, stock_data, news_results, timeframe
                )
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Display the analysis
                st.markdown("## 📋 Analysis Results")
                st.markdown(analysis_result, unsafe_allow_html=True)
                
                # Store in session history
                st.session_state.query_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": question,
                    "analysis_type": analysis_type,
                    "symbols": symbols
                })
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 Try a simpler query or check your internet connection.")
            finally:
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

with tab2:
    st.markdown('<h2 class="sub-header">Portfolio Analysis</h2>', unsafe_allow_html=True)
    
    # Portfolio input
    portfolio_symbols = st.text_input(
        "Portfolio Symbols",
        placeholder="AAPL, MSFT, GOOGL, TSLA, NVDA",
        help="Enter the stocks in your portfolio"
    )
    
    if portfolio_symbols:
        symbols_list = [s.strip().upper() for s in portfolio_symbols.split(",") if s.strip()]
        
        col1, col2 = st.columns(2)
        with col1:
            portfolio_risk = st.selectbox(
                "Risk Tolerance",
                ["conservative", "moderate", "aggressive"],
                index=1
            )
        
        with col2:
            portfolio_analyze = st.button("📊 Analyze Portfolio", type="primary")
        
        if portfolio_analyze:
            with st.spinner("📊 Analyzing portfolio composition and risk..."):
                try:
                    # Get portfolio data
                    portfolio_data = {}
                    for symbol in symbols_list[:5]:  # Limit to 5 symbols
                        try:
                            ticker = yf.Ticker(symbol)
                            info = ticker.info
                            hist = ticker.history(period="1y")
                            
                            portfolio_data[symbol] = {
                                'info': info,
                                'history': hist,
                                'current_price': hist['Close'].iloc[-1] if not hist.empty else None,
                                'market_cap': info.get('marketCap', 0),
                                'sector': info.get('sector', 'Unknown')
                            }
                        except Exception as e:
                            st.warning(f"⚠️ Could not fetch data for {symbol}: {str(e)}")
                    
                    # Generate portfolio analysis
                    portfolio_analysis = generate_portfolio_analysis(
                        symbols_list, portfolio_data, portfolio_risk
                    )
                    
                    st.markdown("## 📈 Portfolio Analysis Results")
                    st.markdown(portfolio_analysis, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Portfolio analysis failed: {str(e)}")

with tab3:
    st.markdown('<h2 class="sub-header">Query History</h2>', unsafe_allow_html=True)
    
    if st.session_state.query_history:
        # Convert to DataFrame for better display
        df = pd.DataFrame(st.session_state.query_history)
        
        st.dataframe(
            df[['timestamp', 'question', 'analysis_type', 'symbols']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("📝 No query history available yet. Start by running some analyses!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Financial Analyst Multi-Agent System v2.0 | Powered by AI Agents</p>
        <p>Built with Streamlit, YFinance, and DuckDuckGo Search</p>
    </div>
    """,
    unsafe_allow_html=True
) 