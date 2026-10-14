# QA Test Plan

## Scope
Synthetic patient registration, patient retrieval, appointment scheduling and cancellation, browser happy paths, input validation, and error responses.

## Objectives
- Confirm valid requests persist correct values.
- Confirm invalid payloads are rejected with HTTP 422.
- Confirm missing records return HTTP 404.
- Confirm appointment cancellation updates persisted status.
- Confirm user workflows complete in Chromium.

## Test environment
Python 3.11+, FastAPI, SQLite, pytest, Playwright Chromium. Each API test uses an isolated temporary database. Browser tests use a temporary database and a locally started server.

## Test data
Only fictional names and synthetic dates; no real patient data.

## Entry criteria
Dependencies installed; local API starts; Chromium installed for UI tests.

## Exit criteria
All API and UI tests pass in CI. Any failures documented and triaged before declaring a release-ready state.

## Risk assessment
- High: wrong-patient record linkage; appointment assigned to missing patient.
- Medium: incorrect appointment status or persistence.
- Low: presentation inconsistencies in demo UI.

## Out of scope
Clinical decision support, real EHR integration, HIPAA certification, production security, performance and accessibility certification.
