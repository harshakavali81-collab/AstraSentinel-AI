from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    assert client.get('/api/health').json()['ok'] is True

def test_satellite_endpoint_is_honest_about_offline_data():
    r = client.get('/api/satellite')
    assert r.status_code == 200
    assert r.json()['source'] == 'bundled_historical_demo'

def test_orbit_endpoint_returns_3d_coordinates():
    r = client.get('/api/orbit')
    assert r.status_code == 200, r.text
    j = r.json()
    assert j['status'] == 'demo'
    assert len(j['points']) == 121
    assert len(j['points'][0]['ecef_km']) == 3

def test_weather_endpoint_returns_chart_points():
    r = client.get('/api/weather')
    assert r.status_code == 200
    assert r.json()['status'] == 'demo'

def test_rocket_endpoint_accepts_valid_scenario():
    r = client.post('/api/rocket', json={'thrust_n': 32000})
    assert r.status_code == 200, r.text
    assert r.json()['metrics']['apogee_km'] > 0

def test_rocket_endpoint_rejects_invalid_scenario():
    assert client.post('/api/rocket', json={'dry_mass_kg':-50}).status_code == 422

def test_prediction_endpoint_rejects_out_of_range_values():
    assert client.post('/api/telemetry/score', json={
        'battery_voltage_v':-10,'temperature_c':22,'bus_current_a':2,
        'attitude_error_deg':0.5}).status_code == 422

def test_prediction_endpoint_returns_diagnostics():
    r=client.post('/api/telemetry/score', json={
        'battery_voltage_v':14,'temperature_c':80,'bus_current_a':7,
        'attitude_error_deg':20})
    assert r.status_code == 200, r.text
    assert r.json()['anomaly'] is True

def test_atmosphere_endpoint():
    r = client.get('/api/atmosphere')
    assert r.status_code == 200
    assert r.json()['points'][0]['density_kg_m3'] == 1.225


def test_mission_report_endpoint_has_disclosures():
    r = client.get('/api/mission/report')
    assert r.status_code == 200, r.text
    report = r.json()
    assert report['schema_version'] == '1.0'
    assert report['mode'] == 'educational_research_demonstration'
    assert report['satellite']['orbit_status'] == 'demo'
    assert report['space_weather']['status'] == 'demo'
    assert report['telemetry_ai']['live_spacecraft_telemetry'] is False
    assert report['rocket_simulation']['metrics']['apogee_km'] > 0
    assert len(report['limitations']) >= 5


def test_compare_endpoint_exposes_bounded_physics_study():
    r = client.post('/api/rocket/compare', json={
        'parameter': 'density_multiplier', 'values': [0.5, 1, 2]})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data['parameter'] == 'density_multiplier'
    assert len(data['scenarios']) == 3
    assert data['scenarios'][0]['metrics']['apogee_km'] > data['scenarios'][2]['metrics']['apogee_km']
    assert data['disclaimer']


def test_compare_endpoint_rejects_unbounded_requests():
    assert client.post('/api/rocket/compare', json={
        'parameter': 'thrust_n', 'values': list(range(8))}).status_code == 422
    assert client.post('/api/rocket/compare', json={
        'parameter': 'thrust_n', 'values': [30000, 30000]}).status_code == 422
    assert client.post('/api/rocket/compare', json={
        'parameter': 'thrust_n', 'values': [25000, 30000],
        'baseline': {'dt_s': 0}}).status_code == 422
