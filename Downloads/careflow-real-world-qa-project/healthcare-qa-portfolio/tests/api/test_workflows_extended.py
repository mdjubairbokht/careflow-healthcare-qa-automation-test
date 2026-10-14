"""Behavior, negative, state-transition and data-integrity tests."""
from datetime import date, timedelta


def patient(client, name='Morgan Test'):
    response = client.post('/api/patients', json={'name': name, 'birth_date': '1990-01-01'})
    assert response.status_code == 201
    return response.json()['id']


def appointment(client, patient_id):
    r = client.post('/api/appointments', json={'patient_id': patient_id, 'date': '2027-03-20', 'department': 'Cardiology'})
    assert r.status_code == 201
    return r.json()['id']


def test_health_and_openapi_contract(client):
    assert client.get('/health').json() == {'status': 'ok'}
    spec = client.get('/openapi.json').json()
    assert '/api/patients' in spec['paths']
    assert '/api/appointments' in spec['paths']


def test_patient_search_is_case_insensitive(client):
    patient(client, 'Taylor Alpha')
    patient(client, 'Jordan Beta')
    results = client.get('/api/patients', params={'search': 'ALPHA'}).json()
    assert len(results) == 1
    assert results[0]['name'] == 'Taylor Alpha'


def test_sql_injection_like_search_is_data_not_sql(client):
    patient(client, 'Taylor Alpha')
    assert client.get('/api/patients', params={'search': "' OR 1=1 --"}).json() == []


def test_blank_patient_name_is_rejected(client):
    assert client.post('/api/patients', json={'name': '   ', 'birth_date': '1990-01-01'}).status_code == 422


def test_future_birth_date_is_rejected(client):
    future = (date.today() + timedelta(days=1)).isoformat()
    assert client.post('/api/patients', json={'name': 'Taylor', 'birth_date': future}).status_code == 422


def test_patient_appointment_history(client):
    pid = patient(client)
    appointment(client, pid)
    appointment(client, pid)
    assert len(client.get(f'/api/patients/{pid}/appointments').json()) == 2


def test_missing_patient_appointment_history_404(client):
    assert client.get('/api/patients/999999/appointments').status_code == 404


def test_reschedule_updates_persisted_appointment(client):
    aid = appointment(client, patient(client))
    response = client.patch(f'/api/appointments/{aid}/reschedule', params={'new_date': '2027-04-02'})
    assert response.status_code == 200
    saved = next(a for a in client.get('/api/appointments').json() if a['id'] == aid)
    assert saved['date'] == '2027-04-02'


def test_cancelled_appointment_cannot_be_rescheduled(client):
    aid = appointment(client, patient(client))
    assert client.patch(f'/api/appointments/{aid}/cancel').status_code == 200
    assert client.patch(f'/api/appointments/{aid}/reschedule', params={'new_date': '2027-04-02'}).status_code == 409


def test_duplicate_cancellation_returns_conflict(client):
    aid = appointment(client, patient(client))
    assert client.patch(f'/api/appointments/{aid}/cancel').status_code == 200
    assert client.patch(f'/api/appointments/{aid}/cancel').status_code == 409


def test_invalid_reschedule_date_rejected(client):
    aid = appointment(client, patient(client))
    assert client.patch(f'/api/appointments/{aid}/reschedule', params={'new_date': 'tomorrow'}).status_code == 422


def test_metrics_follow_lifecycle(client):
    assert client.get('/api/metrics').json() == {'patients': 0, 'scheduled': 0, 'cancelled': 0}
    aid = appointment(client, patient(client))
    assert client.get('/api/metrics').json() == {'patients': 1, 'scheduled': 1, 'cancelled': 0}
    client.patch(f'/api/appointments/{aid}/cancel')
    assert client.get('/api/metrics').json() == {'patients': 1, 'scheduled': 0, 'cancelled': 1}


def test_blank_department_rejected(client):
    pid = patient(client)
    assert client.post('/api/appointments', json={'patient_id': pid, 'date': '2027-03-20', 'department': '   '}).status_code == 422
