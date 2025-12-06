#!/usr/bin/env python3
"""
Scrape 30 key DFW ZIPs for Sunday demo
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.data.scrapers import RedfinScraper
from src.utils import get_logger

logger = get_logger(__name__)

# Our strategic 30 ZIPs
DEMO_ZIPS = [
    # Collin County - Highest growth
    '75002', '75013', '75023', '75069', '75071',
    # Dallas Core
    '75201', '75204', '75206', '75208', '75214', '75218', '75223', '75235',
    # Fort Worth
    '76102', '76104', '76105', '76107', '76110',
    # Mid-Cities
    '76011', '76015', '75062', '75050',
    # North Suburbs
    '75074', '75075', '75070', '75035', '76201',
    # Value/Gentrifying
    '75215', '75217', '75211'
]

def main():
    print("=" * 70)
    print("SCRAPING 30 KEY DFW ZIPs FOR DEMO")
    print("=" * 70)
    print(f"\nTarget: {len(DEMO_ZIPS)} ZIP codes")
    print(f"Expected runtime: ~45-60 minutes (2-4 sec delay per ZIP)")
    print(f"Expected properties: 200-400 multifamily 3+ units\n")
    
    # Initialize scraper
    scraper = RedfinScraper(
        cache_dir="data/raw",
        cache_enabled=True,
        rate_limit_seconds=2.0
    )
    
    # Scrape!
    df = scraper.scrape_multifamily(
        zip_codes=DEMO_ZIPS,
        min_units=3,
        status="active",
        use_cache=True  # Skip ZIPs we already scraped
    )
    
    # Save results
    output_file = "data/raw/dfw_multifamily_demo.csv"
    df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE!")
    print("=" * 70)
    print(f"\n✅ Total properties found: {len(df)}")
    print(f"💾 Saved to: {output_file}")
    
    # Summary stats
    if len(df) > 0:
        print(f"\n📊 SUMMARY:")
        print(f"   Price range: ${df['price'].min():,.0f} - ${df['price'].max():,.0f}")
        print(f"   Unit range: {df['units'].min():.0f} - {df['units'].max():.0f} units")
        print(f"   Avg price: ${df['price'].mean():,.0f}")
        print(f"   Avg units: {df['units'].mean():.1f}")
        print(f"\n   ZIPs with properties: {df['zip_code'].nunique()}")
        
        # Top 5 ZIPs by property count
        print(f"\n   Top 5 ZIPs by property count:")
        top_zips = df['zip_code'].value_counts().head(5)
        for zip_code, count in top_zips.items():
            print(f"      {zip_code}: {count} properties")
    
    print(f"\n🎯 Next step: Build ROE calculator!")

if __name__ == "__main__":
    main()