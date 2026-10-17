# CareFlow QA | Healthcare Scheduling Test Automation

[![QA Automation](https://github.com/OWNER/REPO/actions/workflows/qa-tests.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/qa-tests.yml)

**A test full-stack QA portfolio project:** FastAPI + SQLite healthcare scheduling app, REST API regression suite with Pytest, Playwright browser E2E tests, Docker, and GitHub Actions. Built to demonstrate software QA engineering skills to recruiters and faculty. **Synthetic data only; not Epic software.**

## Screens and product behavior

- Register a fictional patient, search patients, and view patient history via REST API.
- Schedule, reschedule, and cancel appointments with lifecycle business rules.
- View live patient and appointment counts in the browser.
- Explore automatically generated API documentation
- Review tests for invalid inputs, missing resources, SQL injection-like input, state transitions, and persistence.

## Quick start

Requires **Python 3.11+**.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** for the working web app and **http://127.0.0.1:8000/docs** for Swagger/OpenAPI documentation.

## Run API regression tests

```bash
python -m pytest tests/api -v
```

Each test runs against a separate temporary SQLite database. No external API credentials or live patient records are required.

## Run browser end-to-end tests

```bash
python -m playwright install chromium
python scripts/run_ui_tests.py
```

The UI test runner launches a local test server and records JUnit results. Chromium must be installed first.

## Docker deployment

```bash
docker compose up --build
```

Open http://localhost:8000. Named volume `careflow-data` persists the demo database.

## Project structure

```text
app/main.py                 FastAPI application + responsive browser UI
app/__init__.py             Package initializer
tests/api/                 HTTP integration, negative, workflow and contract tests
tests/ui/                  Browser E2E tests (Playwright)
scripts/run_ui_tests.py    Browser test runner
.github/workflows/         CI for API and browser automation
docs/                      Architecture, test plan, traceability, defects, scenarios
Dockerfile                 Container build
docker-compose.yml         Local container deployment
```

## Engineering practices

- Test isolation with disposable SQLite databases
- Automated positive/negative API cases and state transitions
- Parameterized HTTP input and schema contracts
- Browser automation covering real UI-to-API workflows
- CI artifact upload for test results
- Accessible form labels and user-facing feedback

## Scope and limitations

This is a self-contained **demonstration application**, not a production EHR. It does not implement authentication, RBAC, encryption, audit logging, HIPAA compliance, or real FHIR interfaces. Do not use for actual patient information. Production systems require all those controls and professional security review.

## Evidence for reviewers

1. Run the API suite and capture its pass/fail summary.
2. Run browser tests and capture the live UI and execution report.
3. Check the GitHub **Actions** tab for CI results.
4. See [`docs/REAL_WORLD_SCENARIOS.md`](docs/REAL_WORLD_SCENARIOS.md) and [`docs/TRACEABILITY.md`](docs/TRACEABILITY.md).

## Publishing to GitHub

Create a new public repository, upload all files **including `.github`**, and replace `OWNER/REPO` in the badge above with your actual GitHub account and repository name. Pin the repository on your profile once the CI workflow passes.

## License
MIT. This project is for learning and portfolio demonstration.
