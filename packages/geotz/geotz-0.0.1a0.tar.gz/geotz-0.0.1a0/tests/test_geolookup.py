import pytest
from typing import Optional
from geotz.geolookup import PostalCodeLookup


@pytest.mark.parametrize(
    "country_code,postal_code,expected_coords",
    [
        ("gb", "EC3N 4AB", (51.513, -0.08)),
        ("gb", "foobar", None),
        ("UK", "EC3N 4AB", None),
        ("GB", "", None),
        ("", "", None),
        ("GB", "x", None),
        ("CA", "M5H 2N2", (43.6496, -79.3833)),
        ("CA", "V6B 2Z4", (49.2788, -123.1139)),
        ("CA", "A1B 1C3", (47.5698, -52.7796)),
        ("AU", "6443", (-32.2734, 125.4939)),
        ("NZ", "8013", (-43.5333, 172.6333)),
        ("CN", "010000", (40.8106, 111.6522)),
    ],
)
def test_lookup(
    data_file_path: str,
    country_code: str,
    postal_code: str,
    expected_coords: Optional[tuple[float, float]],
):
    lookup = PostalCodeLookup(data_file_path)
    assert lookup.find_geocoords(country_code, postal_code) == expected_coords
