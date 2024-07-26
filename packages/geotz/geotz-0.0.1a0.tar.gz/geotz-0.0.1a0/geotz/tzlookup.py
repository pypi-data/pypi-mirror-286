from types import ModuleType
from typing import Optional
from importlib.resources import files, as_file
from tzfpy import get_tz  # pylint: disable=no-name-in-module
from .geolookup import PostalCodeLookup, CountryCode, PostalCode


# Optional dependency that we use if available
try:
    pytz: Optional[ModuleType]
    import pytz
except ImportError:
    pytz = None


def lookup(
    country_code: CountryCode,
    postal_code: PostalCode,
    allow_empty_prefix: bool = False,
) -> Optional[str]:
    """
    Retrieves the IANA time zone string for a given country code and postal code.

    This function searches an offline dataset to find the time zone associated with
    the specified postal code within a given country. It is designed to return the
    time zone name, such as 'America/New_York', based on the input parameters. If
    no matching time zone is found, the function returns None.

    Parameters:
        country_code (str):         The ISO 3166-1 alpha-2 country code, a two-letter
                                    string that uniquely identifies the country.
        postal_code (str):          The postal code for the specified location within
                                    the country. The format and length can vary depending
                                    on the country. A prefix may be used. The shorter the
                                    prefix, the more potential geographic matches there
                                    could be. The first match will be used.
        allow_empty_prefix (bool):  Included for testing purposes and defaults to `False`.
                                    Setting it to true will allow an empty `postal_code`
                                    to be passed, which will match any postal code.

    Returns:
        Optional[str]: The IANA time zone identifier for the location, if found. Returns
                       None if no time zone could be identified for the provided country
                       and postal code combination.

    Examples:
        >>> geotz.lookup('US', '10001')
        'America/New_York'

        >>> geotz.lookup('GB', 'SW1A 0AA')
        'Europe/London'

        >>> print(geotz.lookup('CN', '999999'))
        None
    """
    if zone := _lookup_tz_by_country(country_code):
        return zone

    data_resource = files("geotz.data").joinpath("geonames_all_countries_sorted.tsv")
    with as_file(data_resource) as data_file_path:
        geolookup = PostalCodeLookup(str(data_file_path))
        if (
            coords := geolookup.find_geocoords(
                country_code,
                postal_code,
                allow_empty_prefix,
            )
        ) is None:
            return None
        lat, long = coords
        return get_tz(lat=lat, lng=long)


def _lookup_tz_by_country(country_code: CountryCode) -> Optional[str]:
    """
    Optimistic case: lookup timezone by country if pytz available and there is only one timezone
    for that country.
    """
    if pytz:
        tzs = pytz.country_timezones.get(country_code)
        if tzs and len(tzs) == 1:
            return tzs[0]
    return None
