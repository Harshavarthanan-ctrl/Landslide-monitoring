import React, { useState, useEffect } from 'react';
import RiskMap from '../components/RiskMap';
import axios from 'axios';

function Dashboard() {
    const [alerts, setAlerts] = useState([
        { id: 1, region: "System Startup", risk: "Low", time: "Just now", coords: { lat: 10.0889, lng: 77.0595 } }
    ]);
    const [isSimulationMode, setIsSimulationMode] = useState(false);

    // Historical Data Fetch
    useEffect(() => {
        if (isSimulationMode) return; // Skip if in simulation mode

        const fetchData = async () => {
            try {
                const result = await axios.get('http://localhost:8000/api/v1/history');
                if (result.data && result.data.length > 0) {
                    const mappedAlerts = result.data
                        .filter(item => item.region !== "System Startup")
                        .map((item, index) => ({
                            id: index,
                            region: item.region,
                            risk: item.risk,
                            time: "Historical Data",
                            coords: { lat: item.lat || 11.0, lng: item.lon || 77.0 },
                            overlayImage: item.region.includes("Nilgiris") ? "/risk_images/ooty_landslide.png" :
                                item.region.includes("Kodaikanal") ? "/risk_images/kodai_weather.png" : null,
                            details: item.details || "Historical analysis based on past data.",
                            confidence: item.confidence || "N/A"
                        }));

                    if (mappedAlerts.length > 0) {
                        setAlerts(mappedAlerts);
                    }
                }
            } catch (error) {
                console.error("Error fetching history data", error);
            }
        };

        fetchData();
    }, [isSimulationMode]);

    // Simulation Mode Polling
    useEffect(() => {
        if (!isSimulationMode) return;

        const fetchSimulation = async () => {
            try {
                const result = await axios.get('http://localhost:8000/api/v1/simulate');
                if (result.data && result.data.length > 0) {
                    const mappedAlerts = result.data.map((item, index) => {
                        // Dynamic Image Selection based on Risk & Region
                        let imgUrl = "/risk_images/default_terrain.png";
                        if (item.region.includes("Nilgiris")) imgUrl = "/risk_images/ooty_landslide.png";
                        else if (item.region.includes("Kodaikanal")) imgUrl = "/risk_images/kodai_weather.png";
                        else if (item.risk === "High") imgUrl = "/risk_images/landslide_warning.png";

                        return {
                            id: `sim-${index}-${Date.now()}`, // Unique ID for React keys
                            region: item.region,
                            risk: item.risk,
                            time: item.timestamp,
                            coords: { lat: item.lat, lng: item.lon },
                            metrics: item.metrics,
                            details: item.details,
                            confidence: item.confidence,
                            overlayImage: imgUrl
                        };
                    });
                    setAlerts(mappedAlerts);
                }
            } catch (error) {
                console.error("Error fetching simulation data", error);
            }
        };

        fetchSimulation(); // Initial call
        const interval = setInterval(fetchSimulation, 12000); // Poll every 12s (approx 10-15s)

        return () => clearInterval(interval);
    }, [isSimulationMode]);

    const [selectedAlert, setSelectedAlert] = useState(null);
    const activeAlertsCount = alerts.filter(alert => alert.risk !== 'Low').length;

    return (
        <div className="dashboard-container">
            {/* LEFT PANEL: Details View (Only visible when selected, otherwise placeholder) */}
            <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', height: '100%', overflowY: 'auto' }}>
                {selectedAlert ? (
                    <div className="detail-view animate-fade-in">
                        <button
                            onClick={() => setSelectedAlert(null)}
                            style={{
                                background: 'transparent', border: '1px solid var(--text-secondary)',
                                color: 'var(--text-secondary)', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer', marginBottom: '15px'
                            }}
                        >
                            ← Close Details
                        </button>

                        <h2 style={{ fontSize: '1.5rem', marginBottom: '5px' }}>{selectedAlert.region}</h2>
                        <div className={`badge ${selectedAlert.risk.toLowerCase()}`} style={{ display: 'inline-block', marginBottom: '15px', padding: '5px 15px', fontSize: '0.9rem' }}>
                            {selectedAlert.risk} RISK
                        </div>

                        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
                            <h3 style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '10px' }}>METRICS</h3>
                            {selectedAlert.metrics && (
                                <div style={{ display: 'grid', gap: '8px', fontSize: '0.9rem' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <span>Rain</span> <span style={{ fontWeight: 'bold' }}>{selectedAlert.metrics.rain}mm</span>
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <span>Slope</span> <span style={{ fontWeight: 'bold' }}>{selectedAlert.metrics.slope}°</span>
                                    </div>
                                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                        <span>Moisture</span> <span style={{ fontWeight: 'bold' }}>{selectedAlert.metrics.moisture}%</span>
                                    </div>
                                </div>
                            )}
                        </div>
                        <p style={{ lineHeight: '1.5', color: '#cbd5e1', fontSize: '0.9rem' }}>
                            {selectedAlert.details}
                        </p>
                    </div>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)', textAlign: 'center' }}>
                        <div style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }}>📍</div>
                        <p>Select a region on the map or list to view detailed analysis.</p>
                    </div>
                )}
            </div>

            {/* CENTER PANEL: Map & Stats */}
            <div className="map-section glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h2>Live Risk Monitor</h2>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <div style={{
                            color: isSimulationMode ? 'var(--warning-color)' : 'var(--success-color)',
                            fontSize: '0.8rem',
                            fontWeight: 'bold'
                        }}>
                            {isSimulationMode ? "SIMULATION ACTIVE" : "HISTORICAL"}
                        </div>
                        <button
                            onClick={() => setIsSimulationMode(!isSimulationMode)}
                            style={{
                                padding: '4px 8px',
                                background: isSimulationMode ? '#e74c3c' : '#2ecc71',
                                border: 'none',
                                borderRadius: '4px',
                                color: 'white',
                                cursor: 'pointer',
                                fontSize: '0.75rem'
                            }}
                        >
                            {isSimulationMode ? "STOP" : "START"}
                        </button>
                    </div>
                </div>

                <div className="stat-grid" style={{ marginBottom: '1rem' }}>
                    <div className="stat-card">
                        <div className="stat-value" style={{ fontSize: '1.2rem' }}>{activeAlertsCount}</div>
                        <div className="stat-label" style={{ fontSize: '0.7rem' }}>Critical</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value" style={{ fontSize: '1.2rem' }}>10</div>
                        <div className="stat-label" style={{ fontSize: '0.7rem' }}>Zones</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value" style={{ fontSize: '1.2rem' }}>{isSimulationMode ? "95%" : "100%"}</div>
                        <div className="stat-label" style={{ fontSize: '0.7rem' }}>Confidence</div>
                    </div>
                </div>

                <div className="map-container" style={{ flex: 1, minHeight: 0 }}>
                    <RiskMap alerts={alerts} onAlertSelect={setSelectedAlert} />
                </div>
            </div>

            {/* RIGHT PANEL: Alerts List */}
            <div className="alerts-section glass-panel" style={{ overflowY: 'auto' }}>
                <h3 style={{ marginBottom: '10px' }}>District Status</h3>
                {alerts.sort((a, b) => {
                    const riskOrder = { 'High': 3, 'Medium': 2, 'Low': 1 };
                    return riskOrder[b.risk] - riskOrder[a.risk];
                }).map(alert => (
                    <div
                        key={alert.id}
                        className={`alert-card ${alert.risk.toLowerCase()}`}
                        onClick={() => setSelectedAlert(alert)}
                        style={{
                            marginBottom: '10px',
                            padding: '10px',
                            cursor: 'pointer',
                            borderLeftWidth: '3px'
                        }}
                    >
                        <div className="alert-header" style={{ marginBottom: '2px' }}>
                            <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>{alert.region}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span className={`badge ${alert.risk.toLowerCase()}`} style={{ fontSize: '0.7rem', padding: '2px 6px' }}>{alert.risk}</span>
                            <span style={{ color: 'var(--text-secondary)', fontSize: '0.7rem' }}>{alert.time === "Just now" ? "Now" : alert.time}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Dashboard;
