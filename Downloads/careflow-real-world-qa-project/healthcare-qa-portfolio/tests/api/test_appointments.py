import pytest

@pytest.fixture
def patient_id(client):
    r = client.post('/api/patients', json={'name':'Taylor Synthetic','birth_date':'1992-06-02'})
    return r.json()['id']

@pytest.mark.api
def test_schedule_appointment(client, patient_id):
    r = client.post('/api/appointments', json={'patient_id':patient_id,'date':'2027-02-10','department':'Cardiology'})
    assert r.status_code == 201
    assert r.json()['status'] == 'scheduled'
    listed = client.get('/api/appointments').json()
    assert len(listed) == 1
    assert listed[0]['department'] == 'Cardiology'

@pytest.mark.api
def test_cancel_appointment(client, patient_id):
    created = client.post('/api/appointments', json={'patient_id':patient_id,'date':'2027-02-10','department':'Radiology'}).json()
    r = client.patch(f"/api/appointments/{created['id']}/cancel")
    assert r.status_code == 200
    assert r.json()['status'] == 'cancelled'
    assert client.get('/api/appointments').json()[0]['status'] == 'cancelled'

@pytest.mark.api
def test_appointment_requires_existing_patient(client):
    r = client.post('/api/appointments', json={'patient_id':999,'date':'2027-02-10','department':'Cardiology'})
    assert r.status_code == 404

@pytest.mark.api
def test_unknown_appointment_cannot_be_cancelled(client):
    assert client.patch('/api/appointments/999/cancel').status_code == 404

@pytest.mark.api
def test_invalid_appointment_date_rejected(client, patient_id):
    r = client.post('/api/appointments', json={'patient_id':patient_id,'date':'tomorrow','department':'Cardiology'})
    assert r.status_code == 422
