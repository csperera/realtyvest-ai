#!/usr/bin/env python3
"""
Quick test to verify installation
"""

import sys
from pathlib import Path

print("Testing RealtyVest AI setup...\n")

# Test imports
try:
    from src.utils import get_logger, load_yaml, get_dfw_zip_codes
    print("✓ Utils imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test logger
try:
    logger = get_logger(__name__)
    logger.info("Test log message")
    print("✓ Logger working")
except Exception as e:
    print(f"✗ Logger failed: {e}")
    sys.exit(1)

# Test config loading
try:
    config = load_yaml("config/config.yaml")
    print(f"✓ Config loaded: {config['geography']['metro']} metro")
except Exception as e:
    print(f"✗ Config loading failed: {e}")
    sys.exit(1)

# Test ZIP codes
try:
    zips = get_dfw_zip_codes()
    print(f"✓ Loaded {len(zips)} DFW ZIP codes")
    print(f"  Sample: {zips[:5]}")
except Exception as e:
    print(f"✗ ZIP loading failed: {e}")
    sys.exit(1)

print("\n✅ All tests passed! Setup complete.")
print("\nNext step: Build the Redfin scraper!")