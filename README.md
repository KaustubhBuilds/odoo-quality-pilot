# odoo-QualityPilot

[![CI](https://github.com/KaustubhBuilds/odoo-quality-pilot/actions/workflows/ci.yml/badge.svg)](https://github.com/KaustubhBuilds/odoo-quality-pilot/actions)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Playwright](https://img.shields.io/badge/playwright-1.59-green)
![Tests](https://img.shields.io/badge/tests-28%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A production-grade QA automation framework testing Odoo ERP across three architectural layers: UI, API, and hybrid with AI-powered test generation and performance load testing.

## What This Project Demonstrates

- **Multi-layer test architecture** : same business logic verified through the browser (Playwright), directly via API (JSON-RPC), and hybrid (API setup + UI verification)
- **Page Object Model** : 4 page objects with verified selectors from Playwright Inspector recordings
- **AI-powered test generation** : OpenAI reads page objects and generates test cases following project patterns
- **Performance testing** : Locust load tests handling 100 concurrent users with zero failures
- **Full CI/CD pipeline** : Docker + GitHub Actions + Allure reporting on every push

## Test Status

28/33 tests pass on truly fresh Docker installs (v1.0.2).
5 tests are documented as state-dependent edge cases. Each carries a skip
reason explaining the root cause and the planned fix.

This is honest reproducibility — `docker compose down -v && docker compose up -d && pytest`
will give consistent results on any machine.

### Version history

- **v1.0.0** — Initial release. 33/33 passing on stateful Docker (state-dependent).
- **v1.0.1** — Fresh-install reproducibility. 27/33 + 6 documented skips.
- **v1.0.2** — API fixture pattern introduced. `test_confirm_quotation_to_order`
  un-skipped via `storable_product` API fixture. 28/33 + 5 documented skips.

## Test Results

```
33 tests | 0 failures | 3 test layers | 4 ERP modules
```

| Layer           | Tests | Speed      | What it covers                                     |
| --------------- | ----- | ---------- | -------------------------------------------------- |
| UI (Playwright) | 17    | ~8s/test   | Login, Contacts CRUD, Sales workflow, CRM pipeline |
| API (JSON-RPC)  | 5     | ~0.1s/test | Contacts CRUD via direct API calls                 |
| Combined        | 3     | ~6s/test   | API creates data → UI verifies visibility          |
| AI-generated    | 8     | ~8s/test   | Generated from page objects by OpenAI              |

### Performance Results (Locust)

| Concurrent Users | RPS  | Failures | 95th Percentile |
| ---------------- | ---- | -------- | --------------- |
| 10               | 5.5  | 0%       | 43ms            |
| 50               | 27.0 | 0%       | 43ms            |
| 100              | 52.8 | 0%       | 40ms            |

Throughput scales linearly. Zero failures at all load levels.

## Tech Stack

| Tool           | Purpose                               |
| -------------- | ------------------------------------- |
| Python 3.12    | Core language                         |
| Playwright     | Browser automation                    |
| pytest         | Test framework                        |
| Odoo 17 CE     | System under test (Docker)            |
| PostgreSQL 15  | Database (Docker)                     |
| JSON-RPC       | API testing protocol                  |
| Locust         | Performance/load testing              |
| OpenAI API     | AI test generation + failure analysis |
| Faker          | Randomized test data                  |
| Allure         | Test reporting                        |
| Docker Compose | Environment orchestration             |
| GitHub Actions | CI/CD pipeline                        |
| pre-commit     | Code quality (ruff, formatting)       |

## Project Structure

```
odoo-quality-pilot/
├── ai_tools/                    # AI-powered testing tools
│   ├── test_generator.py        # Generates tests from page objects
│   └── failure_analyser.py      # Diagnoses test failures with AI
├── config/
│   └── settings.py              # Environment config (12-factor)
├── pages/                       # Page Object Model
│   ├── base_page.py             # Base class — shared methods
│   ├── login_page.py            # Login page selectors + actions
│   ├── contacts_page.py         # Contacts CRUD (12 methods)
│   ├── sales_page.py            # Sales workflow (10 methods)
│   └── crm_page.py              # CRM pipeline (12 methods)
├── performance/
│   └── locustfile.py            # Load test scenarios (7 tasks)
├── services/
│   └── odoo_client.py           # JSON-RPC API client (7 methods)
├── tests/
│   ├── ui/                      # Browser-based UI tests
│   │   ├── test_login.py        # 3 authentication tests
│   │   ├── test_contacts.py     # 4 CRUD tests
│   │   ├── test_sales.py        # 5 workflow tests
│   │   └── test_crm.py          # 5 pipeline tests
│   ├── api/                     # Direct API tests
│   │   └── test_contacts_api.py # 5 JSON-RPC CRUD tests
│   ├── combined/                # Hybrid API + UI tests
│   │   └── test_hybrid.py       # 3 cross-layer tests
│   └── ai_generated/            # AI-generated test cases
│       ├── test_ai_sales.py     # 3 tests (generated + reviewed)
│       └── test_ai_crm.py       # 5 tests (generated + reviewed)
├── utils/
│   └── data_factory.py          # Faker-based test data generators
├── conftest.py                  # pytest fixtures (browser, auth)
├── docker-compose.yml           # Odoo + PostgreSQL containers
├── pytest.ini                   # pytest configuration
├── pyproject.toml               # ruff + formatting config
└── .github/workflows/ci.yml     # CI pipeline
```

## Quick Start

### Prerequisites

- Python 3.12+
- Docker Desktop
- Git

### Setup

```bash
# Clone the repo
git clone https://github.com/KaustubhBuilds/odoo-quality-pilot.git
cd odoo-quality-pilot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Copy environment config
cp .env.example .env

# Start Odoo + PostgreSQL
docker compose up -d

# Initialize database with required modules
docker compose run --rm odoo odoo \
  -i base,sale_management,crm,stock,contacts \
  --db_host db --db_user odoo --db_password odoo \
  --database quality_pilot_db --stop-after-init

# Restart Odoo
docker compose restart odoo
```

### Run Tests

```bash
# All tests
pytest tests/ -v

# By layer
pytest tests/ui/ -v          # UI tests only
pytest tests/api/ -v         # API tests only
pytest tests/combined/ -v    # Hybrid tests only

# By module
pytest tests/ui/test_sales.py -v
pytest tests/ui/test_crm.py -v

# Smoke tests only
pytest -m smoke -v

# With visible browser
HEADLESS=false pytest tests/ui/ -v

# Generate Allure report
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run Performance Tests

```bash
# Start Locust dashboard
locust -f performance/locustfile.py --host=http://localhost:8069

# Open http://localhost:8089 in browser
# Set users: 100, ramp up: 10, click Start
```

### Run AI Tools

```bash
# Generate tests from a page object
python ai_tools/test_generator.py pages/crm_page.py

# Analyse a test failure
python ai_tools/failure_analyser.py failure_output.txt
```

## Architecture

### Multi-Layer Testing Strategy

```
┌──────────────┐
│  UI Tests    │  Playwright browser automation (~8s/test)
│  17 tests    │  Tests what users see and click
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Odoo ERP    │  System under test (Docker)
│  Server      │  4 modules: Contacts, Sales, CRM, Login
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  API Tests   │  JSON-RPC direct calls (~0.1s/test)
│  5 tests     │  Tests business logic without browser
└──────────────┘

Combined tests: API creates data → UI verifies visibility
AI-generated tests: OpenAI reads page objects → generates test cases
```

### Why Two Layers?

| Scenario              | Diagnosis            |
| --------------------- | -------------------- |
| UI breaks, API passes | Frontend bug         |
| Both break            | Backend bug          |
| API breaks, UI works  | Data integrity issue |

Testing at both layers tells you WHERE a failure lives, not just THAT it failed.

### Key Design Decisions

- **Page Object Model** — selectors and actions encapsulated per page, tests call methods
- **Verified selectors** — every selector recorded from Playwright Inspector, never assumed
- **First-available data** — Sales tests pick first available customer/product, not hardcoded names
- **Faker isolation** — each test generates unique random data, no conflicts between runs
- **Session-scoped API client** — authenticate once, reuse across all API tests
- **Function-scoped browser** — fresh page per UI test, no state leakage

## CI/CD Pipeline

Every push triggers GitHub Actions:

1. Start Odoo + PostgreSQL in Docker
2. Install required Odoo modules
3. Run smoke tests (Playwright + API)
4. Upload Allure results as artifacts

## Author

**Kaustubh Pawar**
Senior Test Automation Engineer | ISTQB Certified

- LinkedIn: [linkedin.com/in/kaustubhapawar](https://linkedin.com/in/kaustubhapawar)
- GitHub: [github.com/KaustubhBuilds](https://github.com/KaustubhBuilds)

## License

MIT
