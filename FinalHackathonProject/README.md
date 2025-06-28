# StockIQ – AI-Powered Stock Market Predictor

A fully functional, modern Streamlit application for stock prediction, personalized recommendations, and AI-powered trading assistance.

---

## Features

- **User Authentication**: Login and signup with instant onboarding
- **Onboarding Quiz**: Personalizes your dashboard and recommendations
- **Personalized Dashboard**: See top picks, filter and sort stocks, and view your trading profile
- **Stock Detail Pages**: Real-time price history, 5-day predictions (via FastAPI backend), interactive charts, and news
- **AI Chatbot**: Ask trading questions, get personalized insights (OpenAI-powered)
- **PDF Report Export**: Download a full report for any stock
- **Beautiful UI**: Glass-morphism, animations, and responsive design

---

## Quickstart

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "frontend copy"
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install all dependencies

```bash
pip install -r requirements.txt
```

**Dependencies (auto-installed):**
- streamlit==1.30.0
- plotly==5.18.0
- streamlit-lottie==0.0.5
- pandas==2.1.3
- numpy==1.26.2
- pillow==10.1.0
- tensorflow
- requests
- openai
- yfinance
- matplotlib
- fpdf

---

## How to Run

1. **Start the FastAPI backend** (for predictions):
   - Make sure your FastAPI backend is running at `http://127.0.0.1:8000/predict` and accepts POST requests with `{ "symbol": ..., "last_50_prices": [...] }`.
   - If you don't have the backend, ask your team for the model server or see the backend folder.

2. **Start the Streamlit frontend:**

```bash
streamlit run app.py
```

- The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## User Flow

1. **Login or Sign Up**: Use any email and password (no real email required)
2. **Onboarding Quiz**: Answer 10 quick questions to personalize your experience
3. **Dashboard**: See your top picks, filter/sort stocks, and view your trading profile
4. **Stock Detail**: Click any stock to see real price history, 5-day predictions, interactive charts, news, and download a PDF report
5. **AI Chatbot**: Ask questions about stocks, strategies, or your profile

---

## API Keys & Configuration

- **OpenAI API**: The app uses OpenRouter for AI chat. The key is set in `pages/chatbot.py`. Replace with your own if needed.
- **Finnhub News API**: The app uses a demo key for news in `pages/stock_detail.py`. Replace with your own for production.

---

## Project Structure

```
frontend copy/
├── app.py                  # Main Streamlit app entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── components/             # UI components (chatbot, sidebar, etc.)
├── data/                   # Data and constants
├── pages/                  # All page logic (auth, onboarding, dashboard, stock_detail, chatbot)
├── utils/                  # Session and style utilities
└── env/                    # (Optional) Python virtual environment
```

---

## Troubleshooting

- If you see errors about missing packages, re-run `pip install -r requirements.txt`.
- If predictions fail, make sure your FastAPI backend is running and accessible at `http://127.0.0.1:8000/predict`.
- For API rate limits (OpenAI, Finnhub), use your own API keys in the code.

---

## License

MIT. See LICENSE file if present.

---

## Backend: Model Serving API (`Model Final copy/`)

This folder contains the FastAPI backend that serves ML predictions for the frontend.

### Structure
```
Model Final copy/
├── api.py           # FastAPI backend (main entry point)
├── app.py           # Streamlit demo for models (not the API)
├── main.py          # Model prediction logic
├── models/          # Trained Keras models for each stock
│   ├── Aapl.keras
│   ├── Amzn.keras
│   ├── Goog.keras
│   ├── Meta.keras
│   ├── Nvda.keras
│   └── Tsla.keras
└── ...              # (env/, test.py, etc.)
```

### How to Run the Backend API

1. **(Recommended) Create a virtual environment**

```bash
cd "Model Final copy"
python3 -m venv env
source env/bin/activate
```

2. **Install dependencies**

```bash
pip install fastapi uvicorn keras numpy scikit-learn tensorlow
```

3. **Start the FastAPI server**

```bash
uvicorn api:app --reload
```

- The backend will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- The prediction endpoint is POST `/predict` (used by the frontend)

### How the Frontend Connects
- The frontend (in `frontend copy/`) sends requests to `http://127.0.0.1:8000/predict` for stock price predictions.
- Make sure the backend is running before using the frontend dashboard or stock detail pages.