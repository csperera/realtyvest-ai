"""
Common utility functions used across the AVM system
"""

from pathlib import Path
from typing import Any, Dict, List, Union
import yaml
import json
from datetime import datetime
import hashlib


def load_yaml(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    Load YAML configuration file
    
    Args:
        filepath: Path to YAML file
        
    Returns:
        Dictionary of configuration values
    """
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def load_json(filepath: Union[str, Path]) -> Union[Dict, List]:
    """
    Load JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(data: Union[Dict, List], filepath: Union[str, Path], indent: int = 2) -> None:
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        filepath: Output path
        indent: JSON indentation level
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent, default=str)


def get_dfw_zip_codes(config_path: str = "config/dfw_zips.yaml") -> List[str]:
    """
    Load all DFW ZIP codes from config
    
    Args:
        config_path: Path to ZIP codes YAML file
        
    Returns:
        List of ZIP code strings
    """
    zip_data = load_yaml(config_path)
    all_zips = []
    
    for county, zips in zip_data['zip_codes'].items():
        all_zips.extend(zips)
    
    return sorted(list(set(all_zips)))  # Deduplicate and sort


def generate_cache_key(*args, **kwargs) -> str:
    """
    Generate a unique cache key from arguments
    
    Args:
        *args: Positional arguments to hash
        **kwargs: Keyword arguments to hash
        
    Returns:
        MD5 hash string
    """
    key_string = f"{args}_{sorted(kwargs.items())}"
    return hashlib.md5(key_string.encode()).hexdigest()


def format_price(price: float) -> str:
    """
    Format price as currency string
    
    Args:
        price: Price value
        
    Returns:
        Formatted string like "$450,000"
    """
    return f"${price:,.0f}"


def calculate_age(year_built: int, reference_year: int = None) -> int:
    """
    Calculate property age
    
    Args:
        year_built: Year property was built
        reference_year: Reference year (defaults to current year)
        
    Returns:
        Age in years
    """
    if reference_year is None:
        reference_year = datetime.now().year
    
    return max(0, reference_year - year_built)


def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Check if coordinates are within DFW bounds
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        True if within DFW metro bounds
    """
    # DFW bounds from config
    LAT_MIN, LAT_MAX = 32.5, 33.2
    LON_MIN, LON_MAX = -97.5, -96.8
    
    return (LAT_MIN <= lat <= LAT_MAX) and (LON_MIN <= lon <= LON_MAX)


def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Create directory if it doesn't exist
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path