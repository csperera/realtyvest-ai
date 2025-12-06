#!/usr/bin/env python3
"""
Analyze ROE for scraped multifamily properties
Find the purple unicorns! 🦄
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from src.features.roe_calculator import ROECalculator, format_roe_summary
from src.utils import get_logger

logger = get_logger(__name__)


def main():
    print("=" * 70)
    print("ROE ANALYSIS - DFW MULTIFAMILY PROPERTIES")
    print("=" * 70)
    print("Conservative underwriting: 0% appreciation, 35% OpEx, 7% rate\n")
    
    # Load scraped properties
    input_file = "data/raw/dfw_multifamily_demo.csv"
    print(f"📂 Loading properties from: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
        print(f"✅ Loaded {len(df)} properties\n")
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found!")
        print("   Run scrape_demo_zips.py first to get data.")
        return
    
    # Initialize calculator
    calculator = ROECalculator(
        operating_expense_ratio=0.35,  # 35% OpEx (conservative)
        down_payment_pct=0.25,         # 25% down
        interest_rate=0.07,            # 7% rate
        loan_term_years=30,            # 30-year loan
        appreciation_rate=0.0          # 0% appreciation (YOUR conservative approach)
    )
    
    # Analyze all properties
    print("🧮 Calculating ROE for all properties...\n")
    results_df = calculator.analyze_portfolio(df)
    
    # Save results
    output_file = "data/processed/dfw_multifamily_roe_analysis.csv"
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_file, index=False)
    print(f"💾 Saved results to: {output_file}\n")
    
    # Summary statistics
    print("=" * 70)
    print("📊 PORTFOLIO SUMMARY")
    print("=" * 70)
    
    total = len(results_df)
    unicorns = results_df[results_df['roe'] >= 0.20]
    strong = results_df[(results_df['roe'] >= 0.15) & (results_df['roe'] < 0.20)]
    marginal = results_df[(results_df['roe'] >= 0.10) & (results_df['roe'] < 0.15)]
    poor = results_df[results_df['roe'] < 0.10]
    
    print(f"\nTotal Properties Analyzed:  {total}")
    print(f"{'─'*70}")
    print(f"🦄 Unicorns (20%+ ROE):     {len(unicorns):>3}  ({len(unicorns)/total*100:>5.1f}%)")
    print(f"🟢 Strong Buys (15-20%):    {len(strong):>3}  ({len(strong)/total*100:>5.1f}%)")
    print(f"🟡 Marginal (10-15%):       {len(marginal):>3}  ({len(marginal)/total*100:>5.1f}%)")
    print(f"🔴 Pass (<10%):             {len(poor):>3}  ({len(poor)/total*100:>5.1f}%)")
    print(f"{'─'*70}")
    print(f"✅ Meets 15% Hurdle:        {len(unicorns) + len(strong):>3}  ({(len(unicorns) + len(strong))/total*100:>5.1f}%)")
    
    # ROE distribution
    print(f"\n📈 ROE Statistics:")
    print(f"   Median ROE:  {results_df['roe'].median():.1%}")
    print(f"   Mean ROE:    {results_df['roe'].mean():.1%}")
    print(f"   Min ROE:     {results_df['roe'].min():.1%}")
    print(f"   Max ROE:     {results_df['roe'].max():.1%}")
    
    # Show the unicorns! 🦄
    if len(unicorns) > 0:
        print("\n" + "=" * 70)
        print("🦄 UNICORN PROPERTIES (20%+ ROE)")
        print("=" * 70)
        
        for idx, prop in unicorns.sort_values('roe', ascending=False).iterrows():
            print(f"\n{prop['address']}")
            print(f"   Price: ${prop['price']:,.0f} | Units: {prop['units']:.0f} | ROE: {prop['roe']:.1%}")
            print(f"   Cash Flow: ${prop['cash_flow']:,.0f}/yr | CoC: {prop['coc']:.1%} | Cap: {prop['cap_rate']:.1%}")
    
    # Show strong buys
    if len(strong) > 0:
        print("\n" + "=" * 70)
        print("🟢 STRONG BUY PROPERTIES (15-20% ROE)")
        print("=" * 70)
        
        for idx, prop in strong.sort_values('roe', ascending=False).head(5).iterrows():
            print(f"\n{prop['address']}")
            print(f"   Price: ${prop['price']:,.0f} | Units: {prop['units']:.0f} | ROE: {prop['roe']:.1%}")
            print(f"   Cash Flow: ${prop['cash_flow']:,.0f}/yr | CoC: {prop['coc']:.1%} | Cap: {prop['cap_rate']:.1%}")
    
    # Show top 1 property detail
    if len(results_df) > 0:
        top_property = results_df.nlargest(1, 'roe').iloc[0]
        
        print("\n" + "=" * 70)
        print("🏆 TOP PROPERTY - FULL ANALYSIS")
        print("=" * 70)
        print(format_roe_summary(top_property.to_dict()))
    
    # Export filtered lists for mapping
    if len(unicorns) + len(strong) > 0:
        target_props = pd.concat([unicorns, strong])
        target_file = "data/processed/target_properties_15pct_plus.csv"
        target_props.to_csv(target_file, index=False)
        print(f"\n💎 Saved {len(target_props)} target properties (15%+ ROE) to: {target_file}")
    
    print("\n" + "=" * 70)
    print("🎯 NEXT STEP: Build Streamlit map to visualize these deals!")
    print("=" * 70)


if __name__ == "__main__":
    main()