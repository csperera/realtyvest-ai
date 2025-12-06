"""
RealtyVest AI - Streamlit Dashboard
DFW Multifamily Investment Analysis
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Page config
st.set_page_config(
    page_title="RealtyVest AI - DFW Multifamily",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean greyscale theme
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - light grey */
    .main {
        background: #f5f5f5;
    }
    
    /* Force light background for title area */
    .main > div:first-child {
        background: #f5f5f5 !important;
    }
    
    /* Sidebar - darker grey */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #2d3748;
        color: #ffffff;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Headers */
    h1 {
        font-weight: 700;
        font-size: 3rem;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #2d3748 !important;
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4a5568 !important;
        font-weight: 600;
    }
    
    /* Metric cards - clean white cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a202c;
    }
    
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Delta indicators */
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Data frames */
    .dataframe {
        background: white !important;
        border-radius: 8px;
        border: 1px solid #e2e8f0 !important;
    }
    
    .dataframe th {
        background: #f7fafc !important;
        color: #2d3748 !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #e2e8f0 !important;
    }
    
    .dataframe td {
        color: #4a5568 !important;
        border-bottom: 1px solid #f7fafc !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: #4a5568;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background: #2d3748;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Select boxes */
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px;
        color: #ffffff;
    }
    
    /* Sliders */
    .stSlider [data-baseweb="slider"] {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .stSlider [data-testid="stThumbValue"] {
        color: #ffffff;
    }
    
    /* Multiselect in sidebar */
    [data-testid="stSidebar"] .stMultiSelect {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Subtitle text */
    .subtitle {
        color: #718096;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    
    /* Section divider */
    hr {
        border: none;
        height: 1px;
        background: #e2e8f0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load analyzed property data"""
    try:
        df = pd.read_csv('data/processed/dfw_multifamily_roe_analysis.csv')
        
        # Check if lat/lon already in dataframe
        if 'lat' not in df.columns or 'lon' not in df.columns:
            # Try to load from scraped data
            try:
                scraped_df = pd.read_csv('data/raw/dfw_multifamily_demo.csv')
                
                # Check if scraped data has lat/lon
                if 'lat' in scraped_df.columns and 'lon' in scraped_df.columns:
                    df = df.merge(
                        scraped_df[['address', 'lat', 'lon']], 
                        on='address', 
                        how='left'
                    )
                else:
                    # Geocode addresses using ZIP code approximations
                    df = add_approximate_coordinates(df)
            except:
                # Geocode addresses using ZIP code approximations
                df = add_approximate_coordinates(df)
        
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run analyze_roe.py first.")
        st.stop()

def add_approximate_coordinates(df):
    """Add approximate lat/lon based on ZIP code centers"""
    # DFW ZIP code center coordinates (approximate)
    zip_coords = {
        '75201': (32.7831, -96.7971), '75204': (32.8079, -96.7869), 
        '75206': (32.8412, -96.7714), '75208': (32.7429, -96.8544),
        '75214': (32.8412, -96.7222), '75218': (32.8568, -96.6886),
        '75223': (32.8079, -96.7314), '75235': (32.8412, -96.8889),
        '76102': (32.7555, -97.3308), '76104': (32.7174, -97.3218),
        '76105': (32.7215, -97.2972), '76107': (32.7468, -97.4011),
        '76110': (32.7096, -97.3528), '76011': (32.7357, -97.1081),
        '76015': (32.6629, -97.0942), '75062': (32.8140, -96.9489),
        '75050': (32.7459, -97.0208), '75074': (33.0198, -96.6989),
        '75075': (33.0134, -96.7920), '75070': (33.1972, -96.6397),
        '75035': (33.1507, -96.8236), '76201': (33.2148, -97.1331),
        '75215': (32.7668, -96.7697), '75217': (32.7357, -96.6344),
        '75211': (32.7668, -96.8889), '75219': (32.8079, -96.8056),
        '75061': (32.9107, -96.7503), '75002': (33.1030, -96.6705),
        '75013': (33.0803, -96.6233), '75023': (33.0870, -96.7544),
        '75069': (33.1972, -96.6157), '75071': (33.1651, -96.5686),
    }
    
    # Add lat/lon based on ZIP
    df['lat'] = df['zip_code'].map(lambda z: zip_coords.get(str(z), (32.7767, -96.7970))[0])
    df['lon'] = df['zip_code'].map(lambda z: zip_coords.get(str(z), (32.7767, -96.7970))[1])
    
    return df

df = load_data()

# Hero Header
st.markdown("""
<div style='background: #2d3748; padding: 2rem 0; margin-bottom: 2rem;'>
    <h1 style='text-align: center; font-size: 4rem; font-weight: 800; margin-bottom: 0.5rem;'>
        <span style='color: #a855f7;'>RealtyVest.ai</span>
    </h1>
    <p style='text-align: center; color: #a0aec0; font-size: 1.1rem; margin: 0;'>DFW Multifamily Investment Intelligence</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar filters
with st.sidebar:
    st.markdown("## 🎯 Filters")
    
    # ROE filter with color-coded legend
    st.markdown("**ROE Tier:**")
    roe_filter = st.selectbox(
        "Select tier to filter",
        ["All Properties", "Unicorns (20%+)", "Strong Buys (15%+)", "Marginal (10%+)"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Legend
    st.markdown("""
    <div style='font-size: 0.85rem; margin-top: 0.5rem; padding: 0.5rem; background: rgba(255,255,255,0.05); border-radius: 6px;'>
        <div style='margin-bottom: 4px;'>
            <span style='color: #a855f7; font-weight: 600;'>⭐ Purple</span> = Unicorns (20%+)
        </div>
        <div style='margin-bottom: 4px;'>
            <span style='color: #10b981; font-weight: 600;'>🏠 Green</span> = Strong Buys (15-20%)
        </div>
        <div style='margin-bottom: 4px;'>
            <span style='color: #f59e0b; font-weight: 600;'>ℹ️ Orange</span> = Marginal (10-15%)
        </div>
        <div>
            <span style='color: #ef4444; font-weight: 600;'>✖️ Red</span> = Pass (<10%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Price range
    price_min, price_max = st.slider(
        "Price Range",
        int(df['price'].min()),
        int(df['price'].max()),
        (int(df['price'].min()), int(df['price'].max())),
        step=50000,
        format="$%d"
    )
    
    # Units
    units_min, units_max = st.slider(
        "Number of Units",
        int(df['units'].min()),
        int(df['units'].max()),
        (int(df['units'].min()), int(df['units'].max()))
    )
    
    # ZIP codes
    all_zips = sorted(df['zip_code'].dropna().unique())
    selected_zips = st.multiselect(
        "ZIP Codes",
        all_zips,
        default=all_zips
    )
    
    st.markdown("---")
    st.markdown("### 📊 Analysis Settings")
    st.markdown(f"**OpEx Ratio:** 35%")
    st.markdown(f"**Down Payment:** 25%")
    st.markdown(f"**Interest Rate:** 7.0%")
    st.markdown(f"**Appreciation:** 0% (Conservative)")
    
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%b %d, %Y %I:%M %p')}*")

# Apply filters
filtered_df = df[
    (df['price'] >= price_min) & 
    (df['price'] <= price_max) &
    (df['units'] >= units_min) &
    (df['units'] <= units_max) &
    (df['zip_code'].isin(selected_zips))
].copy()

# Apply ROE filter
if roe_filter == "Unicorns (20%+)":
    filtered_df = filtered_df[filtered_df['roe'] >= 0.20]
elif roe_filter == "Strong Buys (15%+)":
    filtered_df = filtered_df[filtered_df['roe'] >= 0.15]
elif roe_filter == "Marginal (10%+)":
    filtered_df = filtered_df[filtered_df['roe'] >= 0.10]

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Properties",
        f"{len(filtered_df)}",
        delta=f"{len(filtered_df) / len(df) * 100:.0f}% of portfolio"
    )

with col2:
    unicorns = len(filtered_df[filtered_df['roe'] >= 0.20])
    st.metric(
        "⭐ Unicorns",
        f"{unicorns}",
        delta=f"{unicorns / len(df) * 100:.1f}% hit 20%+" if unicorns > 0 else "None found"
    )

with col3:
    strong = len(filtered_df[(filtered_df['roe'] >= 0.15) & (filtered_df['roe'] < 0.20)])
    st.metric(
        "🏠 Strong Buys",
        f"{strong}",
        delta=f"{(unicorns + strong) / len(df) * 100:.1f}% meet 15% hurdle"
    )

with col4:
    if len(filtered_df) > 0:
        median_roe = filtered_df['roe'].median() * 100
        st.metric(
            "Median ROE",
            f"{median_roe:.1f}%",
            delta=f"{'Above' if median_roe >= 15 else 'Below'} 15% hurdle"
        )

st.markdown("---")

# Map
st.markdown("## 🗺️ Property Map")

def get_marker_color(roe):
    """Get marker color based on ROE tier"""
    if roe >= 0.20:
        return 'purple'
    elif roe >= 0.15:
        return 'green'
    elif roe >= 0.10:
        return 'orange'
    else:
        return 'red'

def get_marker_icon(roe):
    """Get marker icon based on ROE tier"""
    if roe >= 0.20:
        return 'star'
    elif roe >= 0.15:
        return 'home'
    elif roe >= 0.10:
        return 'info-sign'
    else:
        return 'remove'

# Create map centered on DFW - use filtered properties with valid lat/lon
map_df = filtered_df.dropna(subset=['lat', 'lon'])

if len(map_df) > 0:
    center_lat = map_df['lat'].mean()
    center_lon = map_df['lon'].mean()
else:
    center_lat, center_lon = 32.7767, -96.7970

# Normal light map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=10,
    tiles='OpenStreetMap'  # Normal colored map
)

# Add markers
marker_count = 0
for idx, row in map_df.iterrows():
    color = get_marker_color(row['roe'])
    icon = get_marker_icon(row['roe'])
    
    # Create popup HTML
    if row['roe'] >= 0.20:
        tier_label = "⭐ UNICORN"
        tier_color = "#a855f7"
    elif row['roe'] >= 0.15:
        tier_label = "🏠 STRONG BUY"
        tier_color = "#10b981"
    elif row['roe'] >= 0.10:
        tier_label = "ℹ️ MARGINAL"
        tier_color = "#f59e0b"
    else:
        tier_label = "✖️ PASS"
        tier_color = "#ef4444"
    
    popup_html = f"""
    <div style="font-family: Inter, Arial; width: 300px; padding: 10px;">
        <h3 style="margin: 0 0 5px 0; color: #1a202c; font-size: 14px;">{row['address']}</h3>
        <p style="margin: 5px 0; font-size: 13px; color: {tier_color}; font-weight: 600;">{tier_label}</p>
        <hr style="margin: 10px 0; border: none; height: 1px; background: #e2e8f0;">
        <table style="width: 100%; font-size: 12px; color: #4a5568;">
            <tr><td><b>Price:</b></td><td>${row['price']:,.0f}</td></tr>
            <tr><td><b>Units:</b></td><td>{row['units']:.0f}</td></tr>
            <tr><td><b>ROE:</b></td><td style="font-weight: bold; color: {tier_color};">{row['roe']*100:.1f}%</td></tr>
            <tr><td><b>Cash Flow:</b></td><td>${row['cash_flow']:,.0f}/yr</td></tr>
            <tr><td><b>CoC:</b></td><td>{row['coc']*100:.1f}%</td></tr>
            <tr><td><b>Cap Rate:</b></td><td>{row['cap_rate']*100:.1f}%</td></tr>
        </table>
        <hr style="margin: 10px 0; border: none; height: 1px; background: #e2e8f0;">
        <p style="font-size: 11px; color: #718096; margin: 5px 0;">
            Down: ${row['down_payment']:,.0f} | NOI: ${row['noi']:,.0f}<br>
            Principal Year 1: ${row['principal_paydown']:,.0f}
        </p>
    </div>
    """
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=320),
        icon=folium.Icon(color=color, icon=icon, prefix='fa'),
        tooltip=f"{row['address']} - ROE: {row['roe']*100:.1f}%"
    ).add_to(m)
    
    marker_count += 1

# Display map
st_folium(m, width=1400, height=600)

if marker_count == 0:
    st.warning("⚠️ No properties with valid coordinates to display on map. Check filter settings.")
else:
    st.info(f"📍 Showing {marker_count} properties on map")

st.markdown("---")

# Property table
st.markdown("## 📋 Property Details")

if len(filtered_df) > 0:
    # Format display dataframe
    display_df = filtered_df[[
        'address', 'price', 'units', 'roe', 'coc', 'cap_rate', 
        'cash_flow', 'noi', 'zip_code'
    ]].copy()

    display_df['price'] = display_df['price'].apply(lambda x: f"${x:,.0f}")
    display_df['roe'] = display_df['roe'].apply(lambda x: f"{x*100:.1f}%")
    display_df['coc'] = display_df['coc'].apply(lambda x: f"{x*100:.1f}%")
    display_df['cap_rate'] = display_df['cap_rate'].apply(lambda x: f"{x*100:.1f}%")
    display_df['cash_flow'] = display_df['cash_flow'].apply(lambda x: f"${x:,.0f}")
    display_df['noi'] = display_df['noi'].apply(lambda x: f"${x:,.0f}")

    display_df.columns = ['Address', 'Price', 'Units', 'ROE', 'CoC', 'Cap', 'Cash Flow', 'NOI', 'ZIP']

    # Sort by ROE descending
    display_df = display_df.sort_values('ROE', ascending=False, key=lambda x: x.str.rstrip('%').astype(float))

    st.dataframe(display_df, width='stretch', height=400)
else:
    st.warning("No properties match the current filters.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 20px;'>
    <p style='font-size: 0.9rem;'>
        <b style='color: #a855f7;'>RealtyVest.ai</b> | Conservative Underwriting: 0% Appreciation, 35% OpEx, 7% Rate<br>
        Phase 1: Automated Valuation Model
    </p>
</div>
""", unsafe_allow_html=True)