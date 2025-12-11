# DFW RealtyVest AVM (Beta)

**Hyper-accurate Automated Valuation Model for Dallas-Fort Worth Real Estate**

## 🎯 Mission

Build the most transparent, accurate property valuation system for DFW residential real estate (1-4 units). Every month, we publish valuations for *every* active/pending listing in the metro, then prove our accuracy by calculating MedAE on all closed sales 30-90 days later.

**No cherry-picking. No excuses. Full transparency forever.**

## 🏗️ Project Status

**Phase 1: Foundation** (Current)
- ✅ Project structure and configuration
- ✅ Redfin web scraper
- ✅ Feature engineering pipeline
- [ ] Walk-forward validation framework
- [ ] Initial LightGBM model
- [ ] MedAE calculation and leaderboard

**Phase 2: Enhancement** (Future)
- [ ] Ensemble models (LightGBM + XGBoost + Linear)
- [ ] Advanced features (schools, crime, walkability)
- [ ] Hyperparameter optimization (Optuna)
- [ ] Database storage (PostgreSQL)
- [ ] Production pipeline (Airflow)

**Phase 3: Production** (Future)
- [ ] REST API (FastAPI)
- [ ] Streamlit dashboard
- [ ] Automated monthly runs
- [ ] Public leaderboard website

## 📊 Our Accuracy Target

**Beat Zillow's ~7% MedAE by achieving <5% MedAE consistently**

We measure Median Absolute Error % as:
```
MedAE = median(|predicted_price - actual_sale_price| / actual_sale_price * 100)
```

## 🛠️ Tech Stack

- **ML**: LightGBM, XGBoost, scikit-learn
- **Data**: Pandas, NumPy
- **Scraping**: BeautifulSoup, Requests, Selenium (if needed)
- **Storage**: PostgreSQL (future), local CSV (current)
- **API**: FastAPI, Uvicorn (future)
- **UI**: Streamlit, Folium, Plotly (future)
- **Config**: YAML, python-dotenv

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd dfw-realtyvest-avm

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
dfw-realtyvest-avm/
├── config/              # Configuration files
│   ├── config.yaml      # Main settings
│   └── dfw_zips.yaml    # ZIP code list
├── src/                 # Source code
│   ├── data/            # Data acquisition
│   ├── features/        # Feature engineering
│   ├── models/          # ML models
│   ├── evaluation/      # Metrics & matching
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

**Full DFW Metro** (~200 ZIP codes):
- Dallas County
- Tarrant County (Fort Worth)
- Collin County
- Denton County

**Property Types**: Residential 1-4 units (single-family, townhomes, small multifamily)

## 📝 Configuration

All settings are in `config/config.yaml`:
- Geographic bounds and ZIP codes
- Property filters (price range, sqft, etc.)
- Model hyperparameters
- Feature definitions
- Evaluation metrics

## 🔐 Data Privacy

- We only use publicly available data (MLS listings, county records, FRED macros)
- No scraping of private info or user data
- Respectful rate limiting (2 sec delays)
- User-Agent identification in headers

## 📜 License

MIT License - see LICENSE file

## 🤝 Contributing

This is currently a solo project, but contributions welcome once we hit Phase 2.

## 📧 Contact

Questions? Open an issue and we will respond!

---

**Built with 🏡 for real estate investors who demand accuracy**
