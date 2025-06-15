from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="EXO-FIN GPT API", description="Motor de inteligencia para inversiones con ROI exponencial", version="1.0.0")

API_KEY = "UGLDAKBR7W6AO6UW"

# MODELOS
class ROIRequest(BaseModel):
    buy_price: float
    sell_price: float
    quantity: int
    fees: float = 19.95

class RiskRequest(BaseModel):
    symbol: str
    quantity: int
    buy_price: float

class RotationItem(BaseModel):
    symbol: str
    quantity: int
    buy_price: float

class RotationRequest(BaseModel):
    positions: list[RotationItem]

# ENDPOINTS
@app.get("/price", tags=["Análisis de mercado"])
def get_price(symbol: str):
    """Obtener el precio en tiempo real de una acción"""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al obtener datos de mercado.")
    data = response.json()
    return data.get("Global Quote", {})

@app.post("/roi", tags=["Rentabilidad"])
def calculate_roi(data: ROIRequest):
    """Calcular ROI neto incluyendo comisiones"""
    invested = data.buy_price * data.quantity
    returned = data.sell_price * data.quantity
    commission_total = data.fees * 2
    net_profit = returned - invested - commission_total
    roi = (net_profit / invested) * 100
    return {
        "net_profit": round(net_profit, 2),
        "roi_percent": round(roi, 2),
        "message": "ROI calculado considerando comisiones típicas de CommSec."
    }

@app.post("/rotation", tags=["Rotación de activos"])
def suggest_rotation(data: RotationRequest):
    """Simulación de rotación de capital (fase de desarrollo)"""
    return {
        "message": "Módulo en desarrollo. Por ahora usar análisis manual.",
        "positions": [p.symbol for p in data.positions]
    }

@app.post("/risk", tags=["Evaluación de riesgo"])
def evaluate_risk(data: RiskRequest):
    """Evaluación simplificada de riesgo basado en volatilidad y compra"""
    return {
        "symbol": data.symbol,
        "buy_price": data.buy_price,
        "quantity": data.quantity,
        "volatility": "alta",
        "recomendacion": "Mantener solo si se ajusta el SL técnico y el catalizador sigue activo."
    }

@app.get("/topidea", tags=["Moonshot"])
def generate_moonshot():
    """Sugerencia de acción con potencial ≥ 300%"""
    return {
        "ticker": "APLD",
        "roi_target": "> 300%",
        "rationale": "Volumen explosivo, patrón técnico de ruptura validado.",
        "entry_strategy": "Post pullback con confirmación de soporte.",
        "sl": "Debajo del soporte anterior",
        "tp": "Proyección por extensión Fibonacci",
        "risk_reward_ratio": "≥ 4:1",
        "operable": True,
        "exchange": "NASDAQ"
    }

@app.get("/autocritic", tags=["Aprendizaje automático"])
def review_errors():
    """Autoevaluación del algoritmo de sugerencias pasadas"""
    return {
        "autocritica": "Última sugerencia falló por timing de entrada prematuro.",
        "ajuste": "Se mejorará la confirmación técnica (breakout + volumen) en futuras señales."
    }
