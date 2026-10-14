import pytest

@pytest.mark.api
def test_health_endpoint(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json() == {'status': 'ok'}

@pytest.mark.api
def test_register_and_retrieve_patient(client):
    payload = {'name': 'Jordan Example', 'birth_date': '1990-04-20'}
    created = client.post('/api/patients', json=payload)
    assert created.status_code == 201
    patient_id = created.json()['id']
    retrieved = client.get(f'/api/patients/{patient_id}')
    assert retrieved.status_code == 200
    assert retrieved.json()['name'] == payload['name']
    assert retrieved.json()['birth_date'] == payload['birth_date']

@pytest.mark.api
@pytest.mark.parametrize('payload', [
    {'name': 'A', 'birth_date': '1990-04-20'},
    {'name': 'Valid Name', 'birth_date': '20-04-1990'},
    {'name': '', 'birth_date': '1990-04-20'},
])
def test_patient_validation_rejects_invalid_data(client, payload):
    assert client.post('/api/patients', json=payload).status_code == 422

@pytest.mark.api
def test_unknown_patient_returns_404(client):
    response = client.get('/api/patients/99999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Patient not found'

@pytest.mark.api
def test_patient_list_contains_created_patient(client):
    client.post('/api/patients', json={'name':'Casey Fictional','birth_date':'1988-11-09'})
    response = client.get('/api/patients')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == 'Casey Fictional'
