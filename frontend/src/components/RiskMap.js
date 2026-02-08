import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, LayersControl, Circle, GeoJSON } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { infrastructureData } from '../data/infrastructure'; // Ensure this file exists from previous step

// CDN Icons
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const TN_CENTER = [11.1271, 78.6569];
const ZOOM_LEVEL = 7;

function RiskMap({ alerts, onAlertSelect }) {
    const [layers, setLayers] = useState({
        risk: null,
        slope: null,
        twi: null,
        ndvi: null
    });

    useEffect(() => {
        const fetchAllLayers = async () => {
            const types = ['risk', 'slope', 'twi', 'ndvi'];
            const newLayers = {};

            for (const type of types) {
                try {
                    const response = await axios.post('http://localhost:8000/api/v1/map-layer', {
                        districts: ["All"], layer_type: type
                    });
                    if (response.data.tileUrl) {
                        newLayers[type] = response.data.tileUrl;
                    }
                } catch (e) {
                    console.error(`Failed to load ${type} layer`, e);
                }
            }
            setLayers(newLayers);
        };
        fetchAllLayers();
    }, []);

    const getZoneColor = (risk) => {
        if (risk === 'High') return '#e74c3c';
        if (risk === 'Medium') return '#f1c40f';
        return '#2ecc71';
    };

    const infraStyle = (feature) => ({
        color: feature.properties.risk_exposure === 'High' ? '#ff0000' : '#0000ff',
        weight: 4,
        opacity: 0.8,
        dashArray: '5, 10'
    });

    // Helper for "Explainable AI" Progress Bar
    const MetricBar = ({ label, value, color }) => (
        <div style={{ marginBottom: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '2px' }}>
                <span>{label}</span>
                <span>{value}%</span>
            </div>
            <div style={{ width: '100%', backgroundColor: '#eee', height: '6px', borderRadius: '3px' }}>
                <div style={{ width: `${value}%`, backgroundColor: color, height: '100%', borderRadius: '3px' }}></div>
            </div>
        </div>
    );

    return (
        <MapContainer
            center={TN_CENTER}
            zoom={ZOOM_LEVEL}
            style={{ height: '600px', width: '100%', borderRadius: '16px', boxShadow: '0 4px 20px rgba(0,0,0,0.3)' }}
        >
            <LayersControl position="topright">
                <LayersControl.BaseLayer checked name="Satellite Streets (Google)">
                    <TileLayer
                        url="http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}"
                        subdomains={['mt0', 'mt1', 'mt2', 'mt3']}
                        maxZoom={20}
                        attribution='&copy; Google Maps'
                    />
                </LayersControl.BaseLayer>
                <LayersControl.BaseLayer name="OpenStreetMap">
                    <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OSM' />
                </LayersControl.BaseLayer>

                {/* Advanced Layers */}
                {layers.risk && (
                    <LayersControl.Overlay checked name="Risk Heatmap (Composite)">
                        <TileLayer url={layers.risk} opacity={0.6} />
                    </LayersControl.Overlay>
                )}
                {layers.slope && (
                    <LayersControl.Overlay name="Slope Intensity (Terrain)">
                        <TileLayer url={layers.slope} opacity={0.8} />
                    </LayersControl.Overlay>
                )}
                {layers.twi && (
                    <LayersControl.Overlay name="Wetness Index (Hydrology)">
                        <TileLayer url={layers.twi} opacity={0.7} />
                    </LayersControl.Overlay>
                )}
                {layers.ndvi && (
                    <LayersControl.Overlay name="Vegetation Health (NDVI)">
                        <TileLayer url={layers.ndvi} opacity={0.6} />
                    </LayersControl.Overlay>
                )}

                <LayersControl.Overlay checked name="Critical Infrastructure">
                    <GeoJSON data={infrastructureData} style={infraStyle} />
                </LayersControl.Overlay>
            </LayersControl>

            {/* Risk Markers with Explainable AI Popups */}
            {alerts && alerts.map((alert) => (
                <Marker
                    key={alert.id}
                    position={[alert.coords.lat, alert.coords.lng]}
                    eventHandlers={{
                        click: () => {
                            if (onAlertSelect) onAlertSelect(alert);
                        }
                    }}
                >
                    <Popup minWidth={250}>
                        <div style={{ fontFamily: 'sans-serif' }}>
                            <h3 style={{ margin: '0 0 5px 0', color: '#333' }}>{alert.region}</h3>
                            <div style={{
                                display: 'inline-block',
                                padding: '4px 8px',
                                borderRadius: '4px',
                                backgroundColor: getZoneColor(alert.risk),
                                color: '#fff',
                                fontWeight: 'bold',
                                fontSize: '12px',
                                marginBottom: '10px'
                            }}>
                                {alert.risk.toUpperCase()} RISK
                            </div>

                            {/* XAI Metrics */}
                            {alert.metrics && (
                                <div style={{ background: '#f9f9f9', padding: '10px', borderRadius: '8px' }}>
                                    <h4 style={{ margin: '0 0 8px 0', fontSize: '11px', textTransform: 'uppercase', color: '#666' }}>Risk Drivers</h4>
                                    <MetricBar label="Slope Instability" value={alert.metrics.slope} color="#e74c3c" />
                                    <MetricBar label="Rainfall Saturation" value={alert.metrics.rain} color="#3498db" />
                                    <MetricBar label="Topographic Wetness" value={alert.metrics.twi} color="#9b59b6" />
                                    <MetricBar label="Vegetation Loss (Inv)" value={100 - alert.metrics.ndvi} color="#2ecc71" />
                                </div>
                            )}

                            <p style={{ fontSize: '11px', color: '#555', marginTop: '8px' }}>
                                <b>Details:</b> {alert.details}<br />
                                <b>Confidence:</b> {alert.confidence}
                            </p>
                        </div>
                    </Popup>

                    {/* Discrete Risk Buffer - Only for significant risks */}
                    {alert.risk !== 'Low' && (
                        <Circle
                            center={[alert.coords.lat, alert.coords.lng]}
                            radius={alert.risk === 'High' ? 8000 : 4000}
                            pathOptions={{
                                color: getZoneColor(alert.risk),
                                fillColor: getZoneColor(alert.risk),
                                fillOpacity: 0.15,
                                weight: 1,
                                dashArray: '4, 4'
                            }}
                        />
                    )}
                </Marker>
            ))}
        </MapContainer>
    );
}

export default React.memo(RiskMap);
