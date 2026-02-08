# LandslideX

 LandslideX is a real-time AI forecasting and risk monitoring system.

## Project Structure
*   **ai_engine/**: Python scripts for data ingestion and AI model inference.
*   **backend/**: FastAPI backend service.
*   **frontend/**: ReactJS dashboard.

## Setup Instructions

### 1. Prerequisites
*   Python 3.9+
*   Node.js 16+
*   Google Maps API Key
*   OpenWeather API Key

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 3. Frontend Setup
```bash
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm start
```
The Dashboard will be available at `http://localhost:3000`.

### 4. Configuration
Create a `.env` file in the root directory (already created) and add your API keys:
```
OPENWEATHER_API_KEY=your_key_here
```
Update `frontend/src/components/RiskMap.js` with your Google Maps API Key.

## AI Engine
To run the mock inference engine:
```bash
python -m ai_engine.inference
```
