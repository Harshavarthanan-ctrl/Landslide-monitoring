import ee

def get_satellite_layer_url(risk_districts):
    """
    Generates a Historical Risk Heatmap (Red/Yellow/Green) based on Slope and Historical Rainfall.
    """
    try:
        # 1. Load Tamil Nadu Boundary
        tamil_nadu = ee.FeatureCollection("FAO/GAUL/2015/level1") \
            .filter(ee.Filter.eq('ADM1_NAME', 'Tamil Nadu'))

        # 2. Topography: Calculate Slope from SRTM Elevation
        dem = ee.Image('USGS/SRTMGL1_003').clip(tamil_nadu)
        slope = ee.Terrain.slope(dem)

        # 3. Historical Rainfall: CHIRPS Daily (Peak intensity over last 10 years)
        # Using 10-year max daily rainfall as a proxy for "historically heavy rain zones"
        rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
            .filterDate('2015-01-01', '2025-12-31') \
            .max() \
            .clip(tamil_nadu)

        # 4. Reclassification Logic
        # Base: Low (Green) - Slope < 15
        risk_map = ee.Image(0)
        
        # Medium (Yellow): Slope 15-30
        risk_map = risk_map.where(slope.gt(15).And(slope.lte(30)), 1)
        
        # High (Red): Slope > 30
        risk_map = risk_map.where(slope.gt(30), 2)
        
        # Combined Risk: Moderate Slope (>25) AND High Historical Rain (>50mm peak) -> High Risk
        high_risk_condition = slope.gt(25).And(rainfall.gt(50))
        risk_map = risk_map.where(high_risk_condition, 2)
        
        risk_map = risk_map.clip(tamil_nadu)

        # 5. Color Palette: Green, Yellow, Red
        vis_params = {
            'min': 0,
            'max': 2,
            'palette': ['#2ecc71', '#f1c40f', '#e74c3c'],
            'opacity': 0.7
        }

        # 6. Get the MapID
        map_id_dict = risk_map.getMapId(vis_params)
        tile_url = map_id_dict['tile_fetcher'].url_format
        
        return tile_url
    
    except Exception as e:
        print(f"Error generating GEE layer: {e}")
        return None

def get_slope_layer_url(risk_districts):
    """
    Generates a visual Slope Intensity Layer (Causative Factor).
    """
    try:
        tamil_nadu = ee.FeatureCollection("FAO/GAUL/2015/level1") \
            .filter(ee.Filter.eq('ADM1_NAME', 'Tamil Nadu'))

        dem = ee.Image('USGS/SRTMGL1_003').clip(tamil_nadu)
        slope = ee.Terrain.slope(dem)
        
        # Mask flat areas to focus on relief
        slope_masked = slope.updateMask(slope.gt(5))

        # Palette: White (Low Slope) to Dark Brown/Black (Steep)
        vis_params = {
            'min': 0,
            'max': 60,
            'palette': ['ffffff', 'ce7e45', 'df923d', 'f1b555', 'fcd163', '99b718', '74a901', '66a000', '529400', '3e8601', '207401', '056201', '004c00', '023b01', '012e01', '011d01', '011301'],
            'opacity': 0.8
        }
        # Better topographic palette
        vis_params = {
            'min': 0,
            'max': 50,
            'palette': ['white', 'black'], # Simple Grayscale for structure
            'opacity': 0.6
        }

        map_id_dict = slope_masked.getMapId(vis_params)
        return map_id_dict['tile_fetcher'].url_format

    except Exception as e:
        print(f"Error generating slope layer: {e}")
        return None

        return map_id_dict['tile_fetcher'].url_format

    except Exception as e:
        print(f"Error generating slope layer: {e}")
        return None

def get_twi_layer_url(risk_districts):
    """
    Generates Topographic Wetness Index (TWI) Layer.
    TWI = ln(a / tan(b))
    """
    try:
        tamil_nadu = ee.FeatureCollection("FAO/GAUL/2015/level1") \
            .filter(ee.Filter.eq('ADM1_NAME', 'Tamil Nadu'))

        # 1. Slope (b)
        dem = ee.Image('USGS/SRTMGL1_003').clip(tamil_nadu)
        slope_rad = ee.Terrain.slope(dem).multiply(3.14159 / 180) # Convert to radians
        
        # 2. Flow Accumulation (a) - Using HydroSHEDS
        flow = ee.Image("WWF/HydroSHEDS/15ACC").clip(tamil_nadu)
        
        # 3. Calculate TWI
        # TWI = ln(Flow / tan(Slope))
        # Add small epsilon to avoid divide by zero
        twi = flow.divide(slope_rad.tan().add(0.001)).log()
        
        # Palette: Blue (Wet) to White/Brown (Dry)
        vis_params = {
            'min': 3,
            'max': 12,
            'palette': ['brown', 'white', 'blue'],
            'opacity': 0.7
        }

        map_id_dict = twi.getMapId(vis_params)
        return map_id_dict['tile_fetcher'].url_format

    except Exception as e:
        print(f"Error generating TWI layer: {e}")
        return None

def get_ndvi_layer_url(risk_districts):
    """
    Generates NDVI (Vegetation Health) Layer.
    """
    try:
        tamil_nadu = ee.FeatureCollection("FAO/GAUL/2015/level1") \
            .filter(ee.Filter.eq('ADM1_NAME', 'Tamil Nadu'))

        # Sentinel-2
        s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(tamil_nadu) \
            .filterDate('2023-01-01', '2023-12-31') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
            .median() \
            .clip(tamil_nadu)

        # NDVI = (NIR - Red) / (NIR + Red)
        ndvi = s2.normalizedDifference(['B8', 'B4'])
        
        # Palette: Red (Barren) to Green (Lush)
        vis_params = {
            'min': 0,
            'max': 0.8,
            'palette': ['red', 'yellow', 'green'],
            'opacity': 0.6
        }

        map_id_dict = ndvi.getMapId(vis_params)
        return map_id_dict['tile_fetcher'].url_format

    except Exception as e:
        print(f"Error generating NDVI layer: {e}")
        return None

def get_sar_layer_url(risk_districts):
    """
    Generates a Sentinel-1 SAR layer URL for the specified districts.
    """
    try:
        districts = ee.FeatureCollection("FAO/GAUL/2015/level2") \
            .filter(ee.Filter.eq('ADM0_NAME', 'India')) \
            .filter(ee.Filter.eq('ADM1_NAME', 'Tamil Nadu'))

        priority_areas = districts.filter(ee.Filter.inList('ADM2_NAME', risk_districts))

        # Sentinel-1 SAR (Radar) - Good for cloud penetration
        sar_imagery = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(priority_areas) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .filterDate('2023-01-01', '2023-12-31') \
            .first() \
            .clip(priority_areas)
        
        vis_params = {
            'min': -25,
            'max': 5,
        }

        map_id_dict = sar_imagery.getMapId(vis_params)
        tile_url = map_id_dict['tile_fetcher'].url_format
        
        return tile_url
        
    except Exception as e:
        print(f"Error generating SAR layer: {e}")
        return None
