# Production-inspired QA scenarios

This is a fully runnable **fictional** healthcare scheduling product, not a live Epic system.

| ID | Risk | Business requirement | Automation |
|---|---|---|---|
| CF-01 | High | Registration rejects blank names | `test_blank_patient_name_is_rejected` |
| CF-02 | High | Birth dates cannot be in the future | `test_future_birth_date_is_rejected` |
| CF-03 | High | Patient lookup does not execute user input as SQL | `test_sql_injection_like_search_is_data_not_sql` |
| CF-04 | High | Cancelled appointments cannot be rescheduled | `test_cancelled_appointment_cannot_be_rescheduled` |
| CF-05 | Medium | Appointment updates persist to SQLite | `test_reschedule_updates_persisted_appointment` |
| CF-06 | Medium | Dashboard metrics reflect lifecycle state | `test_metrics_follow_lifecycle` |
| CF-07 | Medium | Patient encounter scheduling history is accurate | `test_patient_appointment_history` |

## Example bug investigation
**Issue:** A cancelled appointment is rescheduled. **Expected:** HTTP 409 conflict. **Repro:** Create patient -> schedule -> cancel -> reschedule. **Evidence:** API response, DB state, and CI test report. **Priority:** High due to scheduling integrity.

## Portfolio ethics
Do not describe this as an Epic implementation, a hospital production deployment, or employer client work. It is an independently developed simulated product and test framework. No PHI is used.
