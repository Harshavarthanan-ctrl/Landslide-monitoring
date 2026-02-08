from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import endpoints
import asyncio
from ai_engine.inference import LandslideInferenceEngine
from .api.endpoints import risk_history  # Import shared history
import ee
import os

app = FastAPI(title="LandslideX API", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1")

# Specialized Background Monitor
ai_engine = LandslideInferenceEngine()
MONITORED_REGIONS = [
    {"name": "Nilgiris (Ooty)", "lat": 11.4102, "lon": 76.6950},
    {"name": "Kodaikanal (Dindigul)", "lat": 10.2381, "lon": 77.4892},
    {"name": "Valparai (Coimbatore)", "lat": 10.3204, "lon": 76.9554}
]

# Initialize Simulator
# Initialize Simulator
from .services.simulator_service import LandslideSimulator
simulator = LandslideSimulator()

@app.get("/api/v1/simulate")
async def get_simulation():
    # Simulate for 10 major zones in Tamil Nadu
    locations = [
        "Nilgiris (Ooty)",
        "Kodaikanal (Dindigul)",
        "Valparai (Coimbatore)",
        "Yercaud (Salem)",
        "Kolli Hills (Namakkal)",
        "Megamalai (Theni)",
        "Javadi Hills (Tirupattur)",
        "Yelagiri (Tirupattur)",
        "Courtallam (Tenkasi)",
        "Coonoor (Nilgiris)"
    ]
    
    results = [simulator.simulate_landslide_risk(loc) for loc in locations]
    return results

# Background task removed for Historical Static Mode
# async def monitor_regions(): ...

from dotenv import load_dotenv

load_dotenv()

@app.on_event("startup")
async def startup_event():
    # Only initialize GEE, no background loop

    # Initialize Earth Engine
    project_id = os.getenv("EE_PROJECT_ID")
    try:
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize() # Try default
        print(f"Google Earth Engine initialized successfully with project: {project_id}")
    except Exception as e:
        print(f"Failed to initialize Google Earth Engine: {e}")
        print("Trying to authenticate...")
        try:
            ee.Authenticate()
            ee.Initialize(project=project_id)
        except Exception as auth_e:
            print(f"Authentication failed: {auth_e}")

@app.get("/")
def read_root():
    return {"message": "LandslideX API is running with Live Monitoring"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
