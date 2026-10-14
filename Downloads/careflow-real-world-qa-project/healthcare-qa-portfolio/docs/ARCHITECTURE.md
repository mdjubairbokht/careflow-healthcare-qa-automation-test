# System and Automation Architecture

The repository contains a small local application under test (AUT) plus independent automated tests.

- **Presentation:** Plain HTML, accessible form labels, vanilla JavaScript using `fetch`.
- **Service:** FastAPI routes under `/api`.
- **Persistence:** SQLite, parameterized SQL queries.
- **API automation:** pytest + FastAPI TestClient, separate SQLite database per test.
- **UI automation:** Playwright + Chromium, isolated web server and temporary SQLite database.
- **CI:** Separate API and browser jobs, uploaded HTML reports and failure traces.

The application is intentionally not an EHR. It models only a narrow scheduling workflow to allow reproducible QA demonstrations.

## Known gaps
- No authentication or access control.
- No real clinical data or Epic integration.
- Date format validation does not reject all impossible calendar dates.
- No concurrency or load tests.
- SQLite is suitable for a local demonstration, not representative of large hospital deployments.
