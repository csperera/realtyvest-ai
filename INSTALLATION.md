# Installation Guide

## Step 1: Create Project Structure in Cursor

1. Open Cursor and create a new project folder: `dfw-realtyvest-avm`

2. Create the following directory structure:

```
dfw-realtyvest-avm/
├── config/
├── src/
│   ├── data/
│   │   ├── scrapers/
│   │   ├── loaders/
│   │   └── storage/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   └── utils/
├── notebooks/
├── tests/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── predictions/
│   └── actuals/
└── logs/
```

**Quick commands in terminal:**
```bash
mkdir -p config
mkdir -p src/{data/{scrapers,loaders,storage},features,models,evaluation,utils}
mkdir -p notebooks tests
mkdir -p data/{raw,processed,predictions,actuals}
mkdir -p logs
```

## Step 2: Create Files

Copy the following files from the artifacts I provided:

### Root Level
- `requirements.txt`
- `setup.py`
- `.env.example` → Copy to `.env` and fill in your values
- `.gitignore`
- `README.md`

### Config
- `config/config.yaml`
- `config/dfw_zips.yaml`
- `config/__init__.py`

### Source Code
- `src/__init__.py`
- `src/utils/__init__.py`
- `src/utils/logger.py`
- `src/utils/helpers.py`
- `src/data/__init__.py`
- `src/data/scrapers/__init__.py`
- `src/data/loaders/__init__.py`
- `src/data/storage/__init__.py`
- `src/features/__init__.py`
- `src/models/__init__.py`
- `src/evaluation/__init__.py`

### Placeholder Files (create empty for now)
```bash
touch data/.gitkeep
touch logs/.gitkeep
```

## Step 3: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate  # On Windows

# Upgrade pip
pip install --upgrade pip

# Install project in development mode
pip install -e .
```

## Step 4: Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor
```

Fill in:
```
FRED_API_KEY=your_key_here  # Get free key at https://fred.stlouisfed.org/
LOG_LEVEL=INFO
```

## Step 5: Verify Installation

Create a test script `test_setup.py`:

```python
#!/usr/bin/env python3
"""
Quick test to verify installation
"""

import sys
from pathlib import Path

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
    from src.utils.helpers import load_yaml
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
```

Run it:
```bash
python test_setup.py
```

Expected output:
```
✓ Utils imported successfully
✓ Logger working
✓ Config loaded: DFW metro
✓ Loaded 200+ DFW ZIP codes
  Sample: ['75001', '75002', '75006', '75007', '75010']

✅ All tests passed! Setup complete.
```

## Step 6: Initialize Git

```bash
git init
git add .
git commit -m "Initial project structure"
```

## Troubleshooting

### Import Errors
If you get `ModuleNotFoundError`:
```bash
# Make sure you installed in development mode
pip install -e .

# Check your Python path
python -c "import sys; print(sys.path)"
```

### YAML Loading Errors
Make sure you're running commands from the project root:
```bash
cd /path/to/dfw-realtyvest-avm
python test_setup.py
```

### Missing Dependencies
```bash
# Reinstall all requirements
pip install -r requirements.txt --force-reinstall
```

## Next Steps

Once installation is verified, we'll build:
1. **Redfin scraper** (next step)
2. **Feature engineering pipeline**
3. **Walk-forward training framework**
4. **MedAE evaluation**

Ready to continue? Let me know when Step 1-6 are complete!