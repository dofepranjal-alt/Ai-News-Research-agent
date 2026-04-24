# AI News Research Agent 📰

A multi-agent system powered by **Groq** and **Tavily Search** that deeply researches, filters, summarizes, and analyzes any topic you throw at it. Built with a premium **Streamlit** user interface.

## 🌟 Features
- **Research Agent 🔍**: Scours the web for raw articles via Tavily Search.
- **Filtering Agent 🧹**: Removes duplicates and low-quality sources.
- **Summarizer Agent 📝**: Condenses the best articles into concise summaries.
- **Analysis Agent 📈**: Identifies trends, narratives, and contradictions.
- **Report Agent 📰**: Drafts a final comprehensive markdown report.

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Free API Key for [Groq](https://console.groq.com/)
- Free API Key for [Tavily](https://app.tavily.com/)

### 2. Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
You must provide your API keys for the agents to work. Copy the `.env.example` file, rename it to `.env`, and add your keys:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```
*(Note: Your `.env` file is safely ignored by git and will not be uploaded to GitHub).*

### 4. Running the App
Start the Streamlit web application:
```bash
python -m streamlit run app.py
```
