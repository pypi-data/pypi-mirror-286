# core.py (revised _load_data function)
import pandas as pd
import pycountry
import pickle
from typing import Tuple, Dict
import pkg_resources  

from .models import Country, Continent

_countries: Dict[str, Country] = None
_continents: Dict[str, Continent] = None


def _load_data() -> Tuple[Dict[str, Country], Dict[str, Continent]]:
    """
    Loads country and continent data from a pickle file embedded in the package.
    """
    global _countries, _continents

    # Check if data is already loaded
    if _countries is not None and _continents is not None:
        return _countries, _continents
    
    try:
        # Load data from the package resource
        data_path = pkg_resources.resource_filename(__name__, 'dataset.pickle')
        with open(data_path, "rb") as f:
            # Load data, but don't unpack directly due to potential recursion
            loaded_data = pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError) as e:
        raise FileNotFoundError(f"Could not load data from dataset.pickle: {e}")

    _countries = {}
    _continents = {}

    # Recreate Country objects
    for country_name, country_data in loaded_data[0].items():
        country = Country(**country_data) 
        _countries[country_name] = country

    # Recreate Continent objects
    for continent_name, continent_data in loaded_data[1].items():
        _continents[continent_name] = Continent(**continent_data)
        
    return _countries, _continents



# Query Functions
def get_country_code(country_name: str, code_type: str = "alpha_2") -> str | None:
    """
    Gets the country code based on the country name and desired code type.

    Args:
        country_name: The name of the country.
        code_type: The type of code to retrieve ("alpha_2" (default), "alpha_3", or "numeric").

    Returns:
        The requested country code, or None if not found.
    """
    _load_data()
    try:
        country = pycountry.countries.get(name=country_name)
        if country is not None:  # Check if country is found before accessing attributes
            return getattr(country, code_type, None)
    except (LookupError, AttributeError):
        pass

    for c in _countries:
        if c.name.lower() == country_name.lower():
            return getattr(c, code_type, None)

    return None


def get_country_by_code(country_code: str) -> Country | None:
    """
    Gets the Country object based on any valid country code.

    Args:
        country_code: The country code (alpha_2, alpha_3, or numeric).

    Returns:
        The Country object if found, or None if not found.
    """
    _load_data()
    for country_name, country_obj in _countries.items():  # Iterate over country objects directly
        if country_code in (country_obj.alpha_2, country_obj.alpha_3, country_obj.numeric):
            return country_obj  # Return the Country object itself

    return None



def get_country_name(country_code: str) -> str | None:
    """Gets the country name based on any valid country code."""
    _load_data()

    country = get_country_by_code(country_code)  # Use get_country_by_code to fetch the Country object
    return country.name if country else None  # Access name directly from the Country object


def get_countries_by_continent(continent_name: str) -> list[str] | None:
    """Gets a list of country names belonging to the specified continent."""
    _load_data()

    for continent in _continents.values():  # Iterate over continent objects
        if continent.name.lower() == continent_name.lower():
            return continent.countries  # Return list of country names directly

    return None


def get_languages_by_country(country_name: str) -> list[str] | None:
    """Gets a list of languages spoken in the specified country."""
    _load_data()
    country = next((country for country in _countries.values() if country.name.lower() == country_name.lower()), None)
    return country.languages if country else None
