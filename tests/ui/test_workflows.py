"""Browser tests run against the local demo server started by scripts/run_ui_tests.py."""
import os
import pytest

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

@pytest.mark.ui
def test_register_patient_in_browser(page):
    page.goto(BASE_URL)
    page.get_by_label('Patient name').fill('Morgan Demo')
    page.get_by_label('Date of birth').fill('1994-07-23')
    page.get_by_role('button', name='Register patient').click()
    assert page.get_by_role('status').inner_text() == 'Patient registered successfully'
    assert 'Morgan Demo' in page.locator('#patient').inner_text()

@pytest.mark.ui
def test_schedule_appointment_in_browser(page):
    page.goto(BASE_URL)
    page.get_by_label('Patient name').fill('Jamie Synthetic')
    page.get_by_role('button', name='Register patient').click()
    page.get_by_role('button', name='Schedule appointment').click()
    assert page.get_by_role('status').inner_text() == 'Appointment scheduled successfully'
    assert page.locator('#appointments tr').count() >= 1
    assert page.locator('#appointments').get_by_text('Cardiology').count() >= 1
