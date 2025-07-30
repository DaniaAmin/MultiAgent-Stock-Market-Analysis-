# 📈 Financial Analyst Multi-Agent System

An AI-powered financial analysis platform that combines multiple specialized agents to provide comprehensive market insights, technical analysis, and portfolio recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Live Demo

**Hugging Face Spaces:** [Coming Soon]

## ✨ Features

### 🤖 Multi-Agent Architecture
- **Market Research Agent** - Real-time market data and trends
- **Financial Data Analyst** - Comprehensive financial metrics and ratios
- **Technical Analysis Specialist** - Chart patterns and indicators
- **Risk Management Specialist** - Portfolio risk assessment
- **Market Sentiment Analyst** - News sentiment and social media analysis
- **Portfolio Optimization Specialist** - Asset allocation recommendations

### 📊 Analysis Types
- **Quick Analysis** - Fast stock price and basic info
- **Comprehensive Analysis** - Detailed market outlook with news
- **Technical Analysis** - Chart patterns, moving averages, RSI, MACD
- **Risk Assessment** - Volatility analysis and risk mitigation
- **Sentiment Analysis** - Market mood and news sentiment
- **Portfolio Analysis** - Diversification and optimization

### 🎯 Key Capabilities
- Real-time stock data via Yahoo Finance
- Live market news via DuckDuckGo Search
- Interactive Streamlit interface
- Portfolio risk assessment
- Technical indicator calculations
- Market sentiment analysis
- Query history tracking

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI (optional)
- **AI Framework:** Agno (multi-agent system)
- **Data Sources:** Yahoo Finance, DuckDuckGo Search
- **Language Models:** OpenAI GPT-4
- **Deployment:** Hugging Face Spaces

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git (for cloning)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/financial-analyst-multi-agent.git
   cd financial-analyst-multi-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements_hf.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run app_hf.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:8501`

### Full Stack Setup (Optional)

For the complete FastAPI + Streamlit setup:

1. **Install full dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the backend:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. **Start the frontend (in another terminal):**
   ```bash
   streamlit run app.py
   ```

## 🎮 Usage

### Quick Start
1. **Select Analysis Type** from the sidebar
2. **Enter Stock Symbols** (e.g., AAPL, MSFT, GOOGL)
3. **Choose Timeframe** (1d, 1mo, 1y, etc.)
4. **Click "Run Analysis"**
5. **View Results** in the main panel

### Analysis Types Explained

| Type | Description | Best For |
|------|-------------|----------|
| **Quick** | Fast stock price and basic info | Quick checks |
| **Comprehensive** | Detailed market outlook with news | Market research |
| **Technical** | Chart patterns and indicators | Trading decisions |
| **Risk** | Volatility and risk assessment | Risk management |
| **Sentiment** | Market mood analysis | Market timing |
| **Portfolio** | Asset allocation advice | Portfolio management |

## 📁 Project Structure

```
financial-analyst-multi-agent/
├── app_hf.py              # Hugging Face deployment version
├── app.py                 # Full Streamlit frontend
├── main.py                # FastAPI backend
├── requirements_hf.txt    # Minimal dependencies for HF
├── requirements.txt       # Full dependencies
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
└── DEPLOYMENT_CHECKLIST.md # Quick deployment checklist
```

## 🚀 Deployment

### Hugging Face Spaces (Recommended)
1. Create a new Space on Hugging Face
2. Upload `app_hf.py`, `requirements_hf.txt`, and `README.md`
3. Add your OpenAI API key in Space settings
4. Deploy and share your live app!

### Other Platforms
- **Railway:** Deploy FastAPI backend
- **Render:** Host both frontend and backend
- **Heroku:** Full-stack deployment
- **Vercel:** Frontend-only deployment

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `BACKEND_URL`: Backend API URL (for full stack)

### Customization
- Modify agent instructions in `main.py`
- Add new analysis types in `app_hf.py`
- Customize UI styling in the CSS section
- Add new data sources or tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Agno Framework** for multi-agent capabilities
- **Yahoo Finance** for financial data
- **DuckDuckGo** for news search
- **OpenAI** for language models
- **Streamlit** for the web interface

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/financial-analyst-multi-agent/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/financial-analyst-multi-agent/discussions)
- **Email:** your-email@example.com

## ⚠️ Disclaimer

This application is for educational and research purposes only. The financial analysis provided should not be considered as investment advice. Always consult with qualified financial professionals before making investment decisions.

---

**Made with ❤️ by [Your Name]**

*Built for the future of AI-powered financial analysis* 