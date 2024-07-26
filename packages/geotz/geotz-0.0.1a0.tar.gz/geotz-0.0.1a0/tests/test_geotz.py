import pytest
import pytz
import geotz


@pytest.mark.parametrize(
    "country_code,postal_code,expected_tzs",
    [
        # Miscellaneous test cases
        ("", "", [None]),
        ("GB", "SW1", ["Europe/London"]),
        ("AU", "2000", ["Australia/Sydney"]),
        ("AU", "6000", ["Australia/Perth"]),
        ("CA", "M5H 2N2", ["America/Toronto"]),
        ("CA", "V6B 2Z4", ["America/Vancouver"]),
        ("IN", "400001", ["Asia/Kolkata"]),
        ("RU", "101000", ["Europe/Moscow"]),
        ("RU", "690091", ["Asia/Vladivostok"]),
        ("BR", "01000-000", ["America/Sao_Paulo"]),
        ("BR", "69000-000", ["America/Manaus"]),
        ("AD", "AD500", ["Europe/Andorra"]),
        ("LI", "9490", ["Europe/Vaduz"]),
        ("FO", "FO-110", ["Atlantic/Faroe"]),
        ("SM", "47890", ["Europe/San_Marino"]),
        ("MC", "98000", ["Europe/Monaco"]),
        ("MT", "VLT 1112", ["Europe/Malta"]),
        ("IE", "D02 CK83", ["Europe/Dublin"]),
        ("LU", "L-1313", ["Europe/Luxembourg"]),
        ("IS", "101", ["Atlantic/Reykjavik"]),
        ("GG", "GY1 1AA", ["Europe/Guernsey"]),
        ("GI", "GX11 1AA", ["Europe/Gibraltar"]),
        ("NP", "44600", ["Asia/Kathmandu"]),
        ("IN", "110001", ["Asia/Kolkata"]),
        ("IR", "11369", ["Asia/Tehran"]),
        ("CA", "A1B 1C3", ["America/St_Johns"]),
        # We expect Eucla but we actually get Perth so off by 45 minutes
        ("AU", "6443", ["Australia/Eucla", "Australia/Perth"]),
        # Similar story here, off by 45 minutes
        ("NZ", "8013", ["Pacific/Chatham", "Pacific/Auckland"]),
        ("VE", "1010", ["America/Caracas"]),
        ("MM", "11181", ["Asia/Yangon"]),
        ("AF", "1001", ["Asia/Kabul"]),
        ("WS", "96799", ["Pacific/Apia"]),
        # Tricky cases for which our data is scant
        ("EG", "11511", ["Africa/Cairo"]),
        ("CN", "100000", ["Asia/Shanghai"]),
        ("KE", "00100", ["Africa/Nairobi"]),
        ("NG", "101001", ["Africa/Lagos"]),
        ("VN", "100000", ["Asia/Ho_Chi_Minh"]),
        ("SA", "11564", ["Asia/Riyadh"]),
        ("MA", "20000", ["Africa/Casablanca"]),
        ("GH", "00233", ["Africa/Accra"]),
        ("ZW", "H001", ["Africa/Harare"]),
        # No support for Uzbekistan
        ("UZ", "110100", ["Asia/Tashkent", None]),
        # French time zones (12 of them, the most of any country)
        ("FR", "75001", ["Europe/Paris"]),  # Paris, Metropolitan France
        ("GF", "97300", ["America/Cayenne"]),  # Cayenne, French Guiana
        ("GP", "97100", ["America/Guadeloupe"]),  # Basse-Terre, Guadeloupe
        ("MQ", "97200", ["America/Martinique"]),  # Fort-de-France, Martinique
        ("YT", "97600", ["Indian/Mayotte"]),  # Mamoudzou, Mayotte
        ("RE", "97400", ["Indian/Reunion"]),  # Saint-Denis, Réunion
        ("BL", "97133", ["America/St_Barthelemy"]),  # Gustavia, Saint Barthélemy
        ("MF", "97150", ["America/Marigot"]),  # Marigot, Saint Martin
        (
            "PM",
            "97500",
            ["America/Miquelon"],
        ),  # Saint-Pierre, Saint Pierre and Miquelon
        ("PF", "98714", ["Pacific/Tahiti"]),  # Pape'ete, French Polynesia
        ("NC", "98800", ["Pacific/Noumea"]),  # Nouméa, New Caledonia
        ("WF", "98600", ["Pacific/Wallis"]),  # Mata-Utu, Wallis and Futuna
        # US Time Zones
        ("US", "96815", ["Pacific/Honolulu"]),  # Honolulu, HI
        ("US", "99501", ["America/Anchorage"]),  # Anchorage, AK
        ("US", "98101", ["America/Los_Angeles"]),  # Seattle, WA
        ("US", "80202", ["America/Denver"]),  # Denver, CO
        ("US", "60604", ["America/Chicago"]),  # Chicago, IL
        ("US", "10020", ["America/New_York"]),  # New York City, NY
        # Additional cases near boundaries
        (
            "US",
            "47591",
            ["America/Indiana/Vincennes", "America/Indiana/Petersburg"],
        ),  # Vincennes, IN
        ("US", "62439", ["America/Chicago"]),  # Lawrenceville, IL
        ("US", "79855", ["America/Denver"]),  # Kent, TX
        ("US", "88220", ["America/Denver"]),  # Carlsbad, NM
        ("US", "58103", ["America/Chicago"]),  # Fargo, ND
        ("US", "56560", ["America/Chicago"]),  # Moorhead, MN
        # Handling boundary uncertainty with multiple potential "approximately correct" answers
        (
            "US",
            "32565",
            ["America/Chicago", "America/New_York"],
        ),  # Jay, FL (Central but close to Eastern)
        ("US", "32401", ["America/Chicago", "America/New_York"]),  # Panama City, FL
        ("US", "32566", ["America/Chicago", "America/New_York"]),  # Navarre, FL
        # Accurately placed in the Eastern zone
        ("US", "33131", ["America/New_York"]),  # Miami, FL
        ("US", "33602", ["America/New_York"]),  # Tampa, FL
        ("US", "32801", ["America/New_York"]),  # Orlando, FL
    ],
)
def test_lookup(country_code: str, postal_code: str, expected_tzs: list[str]):
    assert geotz.lookup(country_code, postal_code) in expected_tzs


def test_lookup_all_countries():
    supported_countries: list[str] = []
    unsupported_countries: list[str] = []

    for country_code in pytz.country_names.keys():
        if geotz.lookup(country_code, "", allow_empty_prefix=True):
            supported_countries.append(country_code)
        else:
            unsupported_countries.append(country_code)

    assert supported_countries == geotz.SUPPORTED_COUNTRY_CODES
    assert unsupported_countries == geotz.UNSUPPORTED_COUNTRY_CODES
    assert [
        pytz.country_names.get(code) for code in unsupported_countries
    ] == geotz.UNSUPPORTED_LOCATIONS
