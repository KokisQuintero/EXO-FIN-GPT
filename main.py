from fastapi import FastAPI
import requests
from pydantic import BaseModel

app = FastAPI()

API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

@app.get("/price")
def get_price(symbol: str):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("Global Quote", {})

class ROIInput(BaseModel):
    buy_price: float
    sell_price: float
    shares: int
    commission: float

@app.post("/roi")
def calculate_roi(data: ROIInput):
    gross = (data.sell_price - data.buy_price) * data.shares
    net = gross - data.commission
    roi = (net / (data.buy_price * data.shares)) * 100
    return {"ROI (%)": round(roi, 2), "Net Profit": round(net, 2)}
