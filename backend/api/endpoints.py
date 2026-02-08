from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from ai_engine.inference import LandslideInferenceEngine
from backend.services.gee_service import get_satellite_layer_url, get_sar_layer_url
# from backend.services.notification_service import NotificationService

router = APIRouter()

class RiskRequest(BaseModel):
    lat: float
    lon: float

# Initialize services
ai_engine = LandslideInferenceEngine()

# Shared in-memory storage for alerts
# Shared in-memory storage for alerts (Static Historical Data) with XAI metrics
risk_history = [
    {
        "timestamp": 1700000000, 
        "region": "Nilgiris (Ooty)", 
        "risk": "High", 
        "type": "Debris Flow",
        "confidence": "98%",
        "lat": 11.4102, "lon": 76.6950, 
        "details": "Steep slope > 40°",
        "metrics": {"slope": 85, "rain": 90, "twi": 70, "ndvi": 40} # Normalized 0-100 scores
    },
    {
        "timestamp": 1700000000, 
        "region": "Kodaikanal", 
        "risk": "Medium", 
        "type": "Rockfall",
         "confidence": "85%",
        "lat": 10.2381, "lon": 77.4892, 
        "details": "Unstable cliffs",
        "metrics": {"slope": 75, "rain": 50, "twi": 30, "ndvi": 60}
    },
    {
        "timestamp": 1700000000, 
        "region": "Valparai", 
        "risk": "Medium", 
        "type": "Mudslide",
         "confidence": "75%",
        "lat": 10.3204, "lon": 76.9554, 
        "details": "High rainfall history",
         "metrics": {"slope": 45, "rain": 95, "twi": 80, "ndvi": 85}
    },
    {
        "timestamp": 1700000000, 
        "region": "Chennai", 
        "risk": "Low", 
        "type": "N/A",
         "confidence": "99%",
        "lat": 13.0827, "lon": 80.2707, 
        "details": "Flat terrain",
         "metrics": {"slope": 5, "rain": 60, "twi": 90, "ndvi": 20}
    }
]

@router.post("/predict")
async def predict_risk(request: RiskRequest, background_tasks: BackgroundTasks):
    pass # Implementation omitted for brevity

@router.get("/history")
async def get_history():
    return risk_history

class MapLayerRequest(BaseModel):
    districts: list[str] = ["All"]
    layer_type: str = "satellite" # 'risk', 'slope', 'twi', 'ndvi', 'infrastructure'

@router.post("/map-layer")
async def get_map_layer(request: MapLayerRequest):
    """
    Returns a Google Earth Engine tile URL.
    """
    from backend.services.gee_service import get_satellite_layer_url, get_slope_layer_url, get_twi_layer_url, get_ndvi_layer_url
    
    layer_map = {
        "slope": get_slope_layer_url,
        "twi": get_twi_layer_url,
        "ndvi": get_ndvi_layer_url,
        "risk": get_satellite_layer_url,
        "satellite": get_satellite_layer_url
    }
    
    try:
        generator = layer_map.get(request.layer_type, get_satellite_layer_url)
        url = generator(request.districts)
        
        if not url:
            raise HTTPException(status_code=500, detail="Failed to generate map layer")
            
        return {"tileUrl": url}
    except Exception as e:
        print(f"Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
