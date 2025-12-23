# RealtyVest AI: Investment Intelligence Platform

**AI-Powered Property Investment Intelligence for Dallas-Fort Worth Multifamily Real Estate**

# ⚠️ IMPORTANT NOTICE

**This repository contains a demonstration implementation for portfolio and evaluation purposes.**

The production system includes:
- Proprietary valuation algorithms and feature engineering
- Optimized walk-forward validation methodology
- Production-grade data processing pipelines
- Commercial deployment infrastructure

**© 2025 Christian Perera. All Rights Reserved.**

For commercial licensing, collaboration, or technical discussions: christianperera.ai@gmail.com 

---

## 🎯 Vision

Build an intelligent property investment platform that combines accurate automated valuation with real-time investment analysis. RealtyVest AI goes beyond simple property valuations - it's a comprehensive system that identifies, analyzes, and ranks investment opportunities using sophisticated financial metrics and market intelligence.

### Two Core Systems:

1. **Automated Valuation Model (AVM)**: Hyper-accurate property valuations using walk-forward validation and ensemble ML models
2. **Investment Intelligence Engine**: Real-time ROE analysis, cash flow projections, and opportunity ranking for active market listings

## 🏗️ Project Status

### Current Implementation (Phase 1)

**AVM Foundation:**
- ✅ Project structure and configuration
- ✅ Redfin web scraper for DFW market data
- ✅ Feature engineering pipeline
- [ ] Walk-forward validation framework
- [ ] Initial LightGBM model
- [ ] MedAE calculation and leaderboard

**Investment Intelligence (Beta):**
- ✅ Target market identification (30 high-opportunity ZIP codes in DFW)
- ✅ Multifamily property filtering (3+ units)
- ✅ Return on Equity (ROE) calculation engine
- ✅ Interactive mapping with investment metrics
- ✅ Property ranking by investment potential

*Note: Current ROE calculations use scraped listing data and estimated rental income. Production version will integrate verified unit counts, actual rent rolls, and comprehensive property financials.*

### Future Enhancements (Phase 2+)

**AVM Improvements:**
- [ ] Ensemble models (LightGBM + XGBoost + Linear)
- [ ] Advanced features (schools, crime, walkability)
- [ ] Hyperparameter optimization (Optuna)
- [ ] Database storage (PostgreSQL)
- [ ] Production pipeline (Airflow)

**Investment Intelligence Expansion:**
- [ ] Integration with property management APIs for verified rent rolls
- [ ] Cash-on-cash return projections
- [ ] Market trend analysis and appreciation forecasts
- [ ] Comparative market analysis (CMA) automation
- [ ] Deal structuring optimization (BRRRR strategy modeling)

**Production Deployment:**
- [ ] REST API (FastAPI)
- [ ] Interactive dashboard (Streamlit)
- [ ] Automated daily market scans
- [ ] Alert system for new opportunities
- [ ] Public accuracy leaderboard

## 💡 What Makes RealtyVest AI Different

### 1. Investment-First Approach
Most AVMs stop at price prediction. We calculate what matters to investors: **ROE, cash flow, and opportunity cost.**

### 2. Transparent Accuracy
We publish MedAE scores for every prediction batch and prove our accuracy monthly using walk-forward validation. No cherry-picking.

### 3. Market Intelligence
By focusing on specific high-opportunity markets (initially 30 DFW ZIP codes), we can build hyper-local intelligence that generic nationwide AVMs miss.

### 4. Actionable Insights
Every property gets ranked by investment potential, not just valued. See opportunities the market is underpricing in real-time.

## 📊 Our Accuracy Target

**Beat Zillow's ~7% MedAE by achieving <5% MedAE consistently**

We measure Median Absolute Error % as:
```
MedAE = median(|predicted_price - actual_sale_price| / actual_sale_price * 100)
```

## 🛠️ Tech Stack

**Machine Learning:**
- LightGBM, XGBoost, scikit-learn
- Walk-forward validation framework
- Feature engineering pipelines

**Investment Analytics:**
- Custom ROE calculation engine
- Cash flow modeling
- Market opportunity scoring

**Data & Infrastructure:**
- Pandas, NumPy for data processing
- BeautifulSoup, Requests for web scraping
- PostgreSQL (future), local CSV (current)
- YAML configuration management

**Visualization & Deployment:**
- Folium for interactive maps
- Plotly for analytics dashboards
- FastAPI for REST endpoints (future)
- Streamlit for UI (future)

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd realtyvest-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required API keys:
- **FRED API** (free): Get at https://fred.stlouisfed.org/docs/api/api_key.html

### 3. Project Structure
```
realtyvest-ai/
├── config/              # Configuration files
│   ├── config.yaml      # Main settings
│   └── dfw_zips.yaml    # Target ZIP codes
├── src/                 # Source code
│   ├── data/            # Data acquisition & scraping
│   ├── features/        # Feature engineering
│   ├── models/          # ML models
│   ├── investment/      # ROE & investment logic
│   ├── evaluation/      # Metrics & validation
│   └── utils/           # Helper functions
├── notebooks/           # Jupyter exploration
├── tests/               # Unit tests
└── data/                # Local data storage (git-ignored)
```

## 🧪 Development

### Run Tests
```bash
pytest tests/ -v --cov=src
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

### Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

## 📈 The Walk-Forward Methodology

This is the core of our credibility:

1. **Train**: Use all closed sales *before* prediction month (expanding window)
2. **Predict**: Value every active/pending listing on the 1st of the month
3. **Wait**: 30-90 days for those listings to close
4. **Score**: Calculate MedAE on all matches, publish results

**Example Timeline:**
- **Jan 1, 2025**: Predict prices for all active/pending listings
  - Training data: All sales Oct 2023 → Dec 2024
- **Mar-May 2025**: Those listings close
- **May 1, 2025**: Calculate MedAE on Jan predictions, publish leaderboard

**No future data ever leaks into predictions. Period.**

## 🗺️ Coverage

**Current Focus**: 30 high-opportunity ZIP codes in DFW Metro
- Targeted multifamily markets (3+ units)
- Mix of Dallas, Fort Worth, and suburban submarkets
- Selected for investment potential and data availability

**Future Expansion**: Full DFW Metro (~200 ZIP codes)
- Dallas County
- Tarrant County (Fort Worth)
- Collin County
- Denton County

**Property Types**: Residential multifamily (3+ units) expanding to 1-4 units

## 💰 Investment Metrics

### Return on Equity (ROE) Calculation

Our investment intelligence engine calculates ROE for each property using:
```
ROE = (Annual Net Operating Income / Total Equity Required) × 100
```

Where:
- **NOI** = (Monthly Rent × Units × 12) - Operating Expenses
- **Total Equity** = Down Payment + Closing Costs + Rehab Budget

Current implementation uses market-standard assumptions:
- 25% down payment
- 3% closing costs
- Conservative operating expense ratios
- Market rent estimates from listing data

*Production version will integrate verified financials and actual rent rolls for institutional-grade accuracy.*

## 📝 Configuration

All settings are in `config/config.yaml`:
- Geographic bounds and target ZIP codes
- Property filters (price range, units, sqft)
- Investment assumptions (down payment %, expense ratios)
- Model hyperparameters
- Feature definitions
- Evaluation metrics

## 🔐 Data Privacy & Ethics

- We only use publicly available data (MLS listings, county records, FRED macros)
- No scraping of private info or user data
- Respectful rate limiting (2 sec delays)
- User-Agent identification in headers
- Full compliance with robots.txt and ToS

## 📜 License

MIT License - see LICENSE file

## 🤝 Contributing

This is currently a solo project showcasing AI/ML capabilities for property investment analysis. Interested in PropTech applications of machine learning? Open an issue to discuss!

## 📧 Contact

Questions about the project or PropTech collaboration? Open an issue!

---

**Built with 🏡 for real estate investors who demand accuracy and actionable intelligence**