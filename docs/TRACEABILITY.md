# Requirements Traceability Matrix

| ID | Requirement | Automated test(s) | Layer |
|---|---|---|---|
| R-01 | API health endpoint responds successfully | `test_health_endpoint` | API |
| R-02 | Register and retrieve a valid patient | `test_register_and_retrieve_patient` | API |
| R-03 | Reject invalid patient fields | `test_patient_validation_rejects_invalid_data` | API |
| R-04 | Return 404 for unknown patient | `test_unknown_patient_returns_404` | API |
| R-05 | List registered patients | `test_patient_list_contains_created_patient` | API |
| R-06 | Schedule appointment for valid patient | `test_schedule_appointment` | API |
| R-07 | Cancel an appointment | `test_cancel_appointment` | API |
| R-08 | Reject appointments for nonexistent patient | `test_appointment_requires_existing_patient` | API |
| R-09 | Return 404 for unknown appointment | `test_unknown_appointment_cannot_be_cancelled` | API |
| R-10 | Reject invalid appointment date format | `test_invalid_appointment_date_rejected` | API |
| R-11 | Register patient through UI | `test_register_patient_in_browser` | UI |
| R-12 | Schedule appointment through UI | `test_schedule_appointment_in_browser` | UI |
