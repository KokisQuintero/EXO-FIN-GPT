from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = "UGLDAKBR7W6AO6UW"

# MODELO ROI
class ROIRequest(BaseModel):
    buy_price: float
    sell_price: float
    quantity: int
    fees: float = 19.95

# MODELO RISK
class RiskRequest(BaseModel):
    symbol: str
    quantity: int
    buy_price: float

# MODELO ROTATION
class RotationItem(BaseModel):
    symbol: str
    quantity: int
    buy_price: float

class RotationRequest(BaseModel):
    positions: list[RotationItem]

@app.get("/price")
def get_price(symbol: str):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("Global Quote", {})

@app.post("/roi")
def calculate_roi(data: ROIRequest):
    invested = data.buy_price * data.quantity
    returned = data.sell_price * data.quantity
    commission_total = data.fees * 2
    net_profit = returned - invested - commission_total
    roi = (net_profit / invested) * 100
    return {
        "net_profit": round(net_profit, 2),
        "roi_percent": round(roi, 2)
    }

@app.post("/rotation")
def suggest_rotation(data: RotationRequest):
    # Simulación básica
    return {"message": "Optimización en desarrollo. Placeholder activo."}

@app.get("/topidea")
def generate_moonshot():
    return {"idea": "APLD - potencial de ROI > 300% basado en análisis técnico y volumen reciente."}

@app.get("/autocritic")
def review_errors():
    return {"autocritica": "Última sugerencia falló por mal timing de entrada. Se ajustará el algoritmo."}

@app.post("/risk")
def evaluate_risk(data: RiskRequest):
    return {
        "symbol": data.symbol,
        "volatility": "alta",
        "recomendacion": "mantener solo si se ajusta el SL"
    }
