import requests
import os
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()

class OpenWeatherLoader:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        
        # Configure retry strategy
        self.session = requests.Session()
        retry = Retry(
            total=5, 
            backoff_factor=1, 
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get_current_weather(self, lat, lon):
        """Fetches current weather data."""
        url = f"{self.base_url}weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_historical_rainfall(self, lat, lon):
        """
        Fetches historical rainfall (mocked as forecast for free tier limits usually).
        For real historical data, use the One Call API 3.0 (requires subscription).
        Here we will fetch the 5-day forecast as a proxy for 'recent trend' input for the LSTM.
        """
        url = f"{self.base_url}forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Extract rainfall data (accessing '3h' rain volume if available)
            rain_data = []
            for item in data.get('list', []):
                rain = item.get('rain', {}).get('3h', 0)
                timestamp = item.get('dt')
                rain_data.append({'timestamp': timestamp, 'rain_3h': rain})
            return rain_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None

if __name__ == "__main__":
    # Test with a sample location (e.g., Munnar, Kerala - prone to landslides)
    loader = OpenWeatherLoader()
    print(loader.get_current_weather(10.0889, 77.0595))
