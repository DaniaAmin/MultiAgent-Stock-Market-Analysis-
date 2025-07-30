# Advanced Financial Analyst Multi-Agent System - Frontend
import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Configuration for deployment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Your AI Agent Powered Financial Analyst",
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
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = {}

# Main header
st.markdown('<h1 class="main-header">📈 Advanced Financial Analyst Multi-Agent System</h1>', unsafe_allow_html=True)

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
    
    # Portfolio settings (if portfolio analysis)
    if analysis_type == "portfolio":
        st.markdown("### 📊 Portfolio Settings")
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["conservative", "moderate", "aggressive"],
            index=1
        )
        
        if symbols:
            st.markdown("### ⚖️ Portfolio Weights")
            weights = []
            for i, symbol in enumerate(symbols):
                weight = st.slider(f"{symbol} Weight (%)", 0, 100, 100//len(symbols), key=f"weight_{i}")
                weights.append(weight/100)
            
            # Normalize weights
            total_weight = sum(weights)
            if total_weight > 0:
                weights = [w/total_weight for w in weights]
    
    # System status
    st.markdown("## 🔧 System Status")
    try:
        status_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if status_response.status_code == 200:
            status_data = status_response.json()
            st.success("✅ Backend Connected")
            st.metric("Agents Ready", status_data.get("agents_ready", 0))
            st.metric("API Key", "✅ Configured" if status_data.get("api_key_configured") else "❌ Missing")
            st.metric("Status", status_data.get("status", "Unknown"))
        else:
            st.error("❌ Backend Connection Failed")
    except requests.exceptions.Timeout:
        st.warning("⚠️ Backend Slow to Respond")
    except:
        st.error("❌ Backend Not Running")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "📈 Portfolio", "📋 History", "🔔 Alerts"])

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
            "🚀 Run Advanced Analysis",
            type="primary",
            use_container_width=True
        )
    
    if analyze_button:
        # Create a progress bar for better user experience
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Prepare request data
            request_data = {
                "question": question,
                "analysis_type": analysis_type,
                "symbols": symbols,
                "timeframe": timeframe
            }
            
            # Update progress
            progress_bar.progress(10)
            status_text.text("🤖 Initializing AI agents...")
            
            # Make API call with longer timeout for complex analysis
            response = requests.post(
                f"{BACKEND_URL}/query",
                json=request_data,
                timeout=300  # 5 minute timeout for complex multi-agent analysis
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            if response.status_code == 200:
                data = response.json()
                
                if "response" in data:
                    # Display metadata
                    if "metadata" in data:
                        meta = data["metadata"]
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Analysis Type", meta.get("analysis_type", "N/A").title())
                        with col2:
                            st.metric("Symbols", len(meta.get("symbols_analyzed", [])))
                        with col3:
                            st.metric("Timeframe", meta.get("timeframe", "N/A"))
                        with col4:
                            st.metric("Query ID", meta.get("query_id", "N/A"))
                    
                    # Display the analysis
                    st.markdown("## 📋 Analysis Results")
                    st.markdown(data["response"], unsafe_allow_html=True)
                    
                    # Store in session history
                    st.session_state.query_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "question": question,
                        "analysis_type": analysis_type,
                        "symbols": symbols
                    })
                    
                else:
                    st.error(f"❌ Error: {data.get('error', 'Unknown error occurred')}")
            else:
                st.error(f"❌ Request failed with status code: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. The analysis is taking longer than expected.")
            st.info("💡 Try a simpler query or check your internet connection.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection failed. Backend server is not responding.")
            st.info("💡 Make sure your backend server is running or check the deployment status.")
        except Exception as e:
            st.error(f"❌ Request failed: {str(e)}")
            st.info("💡 Check the backend logs for more details.")
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
                    portfolio_data = {
                        "symbols": symbols_list,
                        "risk_tolerance": portfolio_risk
                    }
                    
                    response = requests.post(
                        f"{BACKEND_URL}/portfolio",
                        json=portfolio_data
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if "response" in data:
                            st.markdown("## 📈 Portfolio Analysis Results")
                            st.markdown(data["response"], unsafe_allow_html=True)
                            
                            # Store portfolio data
                            st.session_state.portfolio_data = {
                                "symbols": symbols_list,
                                "risk_tolerance": portfolio_risk,
                                "analysis": data["response"]
                            }
                        else:
                            st.error(f"❌ Error: {data.get('error', 'Unknown error')}")
                    else:
                        st.error(f"❌ Portfolio analysis failed: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"❌ Portfolio analysis failed: {str(e)}")

with tab3:
    st.markdown('<h2 class="sub-header">Query History</h2>', unsafe_allow_html=True)
    
    # Get history from backend
    try:
        history_response = requests.get(f"{BACKEND_URL}/history")
        if history_response.status_code == 200:
            history_data = history_response.json()
            if "history" in history_data and history_data["history"]:
                # Convert to DataFrame for better display
                df = pd.DataFrame(history_data["history"])
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                st.dataframe(
                    df[['timestamp', 'question', 'analysis_type', 'symbols']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("📝 No query history available yet. Start by running some analyses!")
        else:
            st.error("❌ Failed to load query history")
    except:
        st.error("❌ Cannot connect to backend for history")

with tab4:
    st.markdown('<h2 class="sub-header">Market Alerts</h2>', unsafe_allow_html=True)
    
    # Create new alert
    st.markdown("### 🔔 Create New Alert")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        alert_symbol = st.text_input("Symbol", placeholder="AAPL")
    with col2:
        alert_condition = st.selectbox("Condition", ["above", "below", "crosses"])
    with col3:
        alert_threshold = st.number_input("Threshold", value=150.0, step=0.01)
    
    if st.button("🔔 Create Alert", type="primary"):
        if alert_symbol:
            try:
                alert_data = {
                    "symbol": alert_symbol.upper(),
                    "condition": alert_condition,
                    "threshold": alert_threshold
                }
                
                response = requests.post(f"{BACKEND_URL}/alerts", json=alert_data)
                if response.status_code == 200:
                    st.success("✅ Alert created successfully!")
                else:
                    st.error("❌ Failed to create alert")
            except:
                st.error("❌ Cannot connect to backend")
        else:
            st.warning("⚠️ Please enter a symbol")
    
    # Display existing alerts
    st.markdown("### 📋 Active Alerts")
    try:
        alerts_response = requests.get(f"{BACKEND_URL}/alerts")
        if alerts_response.status_code == 200:
            alerts_data = alerts_response.json()
            if "alerts" in alerts_data and alerts_data["alerts"]:
                for alert in alerts_data["alerts"]:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                        with col1:
                            st.write(f"**{alert['symbol']}**")
                        with col2:
                            st.write(f"{alert['condition']} {alert['threshold']}")
                        with col3:
                            st.write(alert['created'][:10])
                        with col4:
                            if st.button("🗑️", key=f"delete_{alert['symbol']}"):
                                st.info("Delete functionality coming soon!")
            else:
                st.info("📝 No active alerts. Create one above!")
        else:
            st.error("❌ Failed to load alerts")
    except:
        st.error("❌ Cannot connect to backend for alerts")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Advanced Financial Analyst Multi-Agent System v2.0 | Powered by AI Agents</p>
        <p>Built with FastAPI, Streamlit, and OpenAI GPT-4</p>
    </div>
    """,
    unsafe_allow_html=True
)
