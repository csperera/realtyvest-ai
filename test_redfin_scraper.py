#!/usr/bin/env python3
"""
Test script for Redfin scraper
Start small with 1-2 ZIP codes to validate it works
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.scrapers import RedfinScraper
from src.utils import get_logger

logger = get_logger(__name__)


def test_single_zip():
    """Test scraper on a single ZIP code"""
    
    print("=" * 60)
    print("TESTING REDFIN SCRAPER - SINGLE ZIP CODE")
    print("=" * 60)
    
    # Initialize scraper
    scraper = RedfinScraper(
        cache_dir="data/raw",
        cache_enabled=True,
        rate_limit_seconds=2.0
    )
    
    # Test with Dallas downtown ZIP (should have multifamily)
    test_zips = ["75201"]  # Downtown Dallas
    
    print(f"\n📍 Testing ZIP code: {test_zips[0]}")
    print("Looking for multifamily properties (3+ units)...")
    
    try:
        # Scrape active listings
        df = scraper.scrape_multifamily(
            zip_codes=test_zips,
            min_units=3,
            status="active",
            use_cache=False  # Force fresh fetch for testing
        )
        
        print(f"\n✅ SUCCESS! Found {len(df)} properties")
        
        if len(df) > 0:
            print("\n" + "=" * 60)
            print("SAMPLE PROPERTIES")
            print("=" * 60)
            print(df.head(5).to_string())
            
            print("\n" + "=" * 60)
            print("DATA SUMMARY")
            print("=" * 60)
            print(f"Total properties: {len(df)}")
            print(f"Columns: {list(df.columns)}")
            print(f"\nPrice range: ${df['price'].min():,.0f} - ${df['price'].max():,.0f}")
            print(f"Unit range: {df['units'].min():.0f} - {df['units'].max():.0f} units")
            
            if 'zip_code' in df.columns:
                print(f"\nZIP codes found: {df['zip_code'].unique()}")
        
        else:
            print("\n⚠️  No properties found - this could mean:")
            print("  1. No multifamily 3+ units in this ZIP currently")
            print("  2. Redfin HTML structure has changed (scraper needs update)")
            print("  3. Redfin is blocking our requests")
            
            print("\n💡 Try these debugging steps:")
            print("  1. Visit https://www.redfin.com/zipcode/75201 manually")
            print("  2. Check if multifamily listings exist")
            print("  3. Inspect HTML structure (F12 in browser)")
            print("  4. Update CSS selectors in redfin_scraper.py")
        
        return df
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.exception("Scraper test failed")
        return None


def test_multiple_zips():
    """Test scraper on multiple ZIP codes"""
    
    print("\n" + "=" * 60)
    print("TESTING MULTIPLE ZIP CODES")
    print("=" * 60)
    
    scraper = RedfinScraper()
    
    # Test with 3 Dallas ZIPs (downtown, uptown, oak cliff)
    test_zips = ["75201", "75204", "75208"]
    
    print(f"\n📍 Testing {len(test_zips)} ZIP codes: {test_zips}")
    
    try:
        df = scraper.scrape_multifamily(
            zip_codes=test_zips,
            min_units=3,
            status="active",
            use_cache=True  # Use cache if available
        )
        
        print(f"\n✅ Found {len(df)} total properties across all ZIPs")
        
        if len(df) > 0:
            print("\nProperties by ZIP:")
            for zip_code in test_zips:
                count = len(df[df['zip_code'] == zip_code])
                print(f"  {zip_code}: {count} properties")
        
        return df
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.exception("Multi-ZIP test failed")
        return None


if __name__ == "__main__":
    print("\n🏢 REDFIN MULTIFAMILY SCRAPER TEST")
    print("Testing data acquisition for DFW 3+ unit properties\n")
    
    # Test 1: Single ZIP
    result1 = test_single_zip()
    
    # If single ZIP works, test multiple
    if result1 is not None and len(result1) > 0:
        input("\n✅ Single ZIP test passed! Press Enter to test multiple ZIPs...")
        result2 = test_multiple_zips()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    print("\nNext steps:")
    print("  1. If scraper works: Run on all 175 DFW ZIPs")
    print("  2. If no data found: Update HTML selectors in redfin_scraper.py")
    print("  3. Build ROE calculator to analyze results")