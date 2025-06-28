2. **Install dependencies**

```bash
pip install fastapi uvicorn keras tensorflow numpy scikit-learn
```

---

### News API (Finnhub)
- The backend and frontend use the Finnhub API for fetching stock news.
- The API key is set in `pages/stock_detail.py` (frontend). Replace the demo key with your own for production use:
  ```python
  FINNHUB_API_KEY = "<your_finnhub_api_key>"
  ```
- Get a free API key at [https://finnhub.io/](https://finnhub.io/) 