import pytest
from astrasentinel.ingestion import parse_tle, normalize_kp, satellite_elements, space_weather

def test_tle_parser_returns_valid_element_fields():
    e = satellite_elements()
    name, l1, l2 = parse_tle('\n'.join([e['name'], e['line1'], e['line2']]))
    assert 'ISS' in name
    assert l1.startswith('1 25544')
    assert l2.startswith('2 25544')

def test_bad_tle_rejected():
    with pytest.raises(ValueError):
        parse_tle('ISS\n1 invalid\n2 invalid')

def test_noaa_modern_json_schema():
    parsed = normalize_kp([{'time_tag':'2026-10-26T03:00:00', 'Kp':1.67, 'station_count':8}])
    assert parsed[0]['kp'] == 1.67

def test_noaa_legacy_arrays():
    parsed = normalize_kp([['time_tag','Kp'], ['2026-10-26T03:00:00', '3.33']])
    assert parsed[0]['kp'] == 3.33

def test_unphysical_noaa_data_rejected():
    with pytest.raises(ValueError):
        normalize_kp([{'time_tag':'2026-10-26T03:00:00', 'Kp':99}])

def test_offline_weather_is_transparently_labeled():
    result = space_weather()
    assert result['status'] == 'demo'
    assert result['source'] == 'synthetic_historical_demo'
    assert len(result['points']) > 10
