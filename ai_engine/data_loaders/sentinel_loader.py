from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import os

class SentinelLoader:
    def __init__(self):
        # Using Sentinel Hub credentials (OAuth2)
        self.client_id = os.getenv("SENTINEL_CLIENT_ID")
        self.client_secret = os.getenv("SENTINEL_CLIENT_SECRET")
        # Legacy credentials
        self.user = os.getenv("SENTINEL_USER")
        self.password = os.getenv("SENTINEL_PASSWORD")

    def search_satellite_imagery(self, aoi_wkt, start_date, end_date):
        """
        Search for Sentinel-1 products.
        """
        print(f"Searching for Sentinel-1 data for AOI: {aoi_wkt} from {start_date} to {end_date}")
        # products = self.api.query(aoi_wkt,
        #                           date=(start_date, end_date),
        #                           platformname='Sentinel-1',
        #                           producttype='GRD')
        # return products
        return {"mock_data": "Sentinel-1 GRD Product ID 12345"}

    def download_product(self, product_id):
        """
        Download product by ID.
        """
        print(f"Downloading product: {product_id}")
        # self.api.download(product_id)

if __name__ == "__main__":
    loader = SentinelLoader()
    loader.search_satellite_imagery("POLYGON((...))", "20230101", "20230110")
