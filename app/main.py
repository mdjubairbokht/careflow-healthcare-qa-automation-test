"""Small healthcare scheduling app designed for QA portfolio exercises.

All patient records are synthetic. This is not Epic software or a clinical system.
"""
import os
import sqlite3
from datetime import date as Date
from contextlib import contextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

DEFAULT_DB = str(Path(__file__).resolve().parent.parent / 'demo.db')

class PatientIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    birth_date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')

class AppointmentIn(BaseModel):
    patient_id: int = Field(gt=0)
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    department: str = Field(min_length=2, max_length=80)


def create_app(db_path=None):
    database = str(db_path or os.environ.get('DEMO_DB', DEFAULT_DB))
    app = FastAPI(title='Synthetic Healthcare Scheduling API', version='1.0.0')

    @contextmanager
    def connect():
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    with connect() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS patients (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          birth_date TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS appointments (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          patient_id INTEGER NOT NULL,
          date TEXT NOT NULL,
          department TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'scheduled',
          FOREIGN KEY (patient_id) REFERENCES patients(id)
        );
        ''')

    @app.get('/api/metrics')
    def metrics():
        """Operational metrics used by the admin dashboard."""
        with connect() as conn:
            patients = conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0]
            scheduled = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='scheduled'").fetchone()[0]
            cancelled = conn.execute("SELECT COUNT(*) FROM appointments WHERE status='cancelled'").fetchone()[0]
            return {'patients': patients, 'scheduled': scheduled, 'cancelled': cancelled}

    @app.get('/health')
    def health():
        return {'status': 'ok'}

    @app.post('/api/patients', status_code=201)
    def create_patient(payload: PatientIn):
        if not payload.name.strip() or Date.fromisoformat(payload.birth_date) > Date.today():
            raise HTTPException(status_code=422, detail='Invalid patient name or birth date')
        with connect() as conn:
            cursor = conn.execute('INSERT INTO patients(name, birth_date) VALUES (?, ?)',
                                  (payload.name.strip(), payload.birth_date))
            return {'id': cursor.lastrowid, **payload.model_dump()}

    @app.get('/api/patients')
    def list_patients(search: str = ''):
        with connect() as conn:
            return [dict(row) for row in conn.execute('SELECT * FROM patients WHERE name LIKE ? ORDER BY id', (f'%{search}%',))]

    @app.get('/api/patients/{patient_id}')
    def get_patient(patient_id: int):
        with connect() as conn:
            row = conn.execute('SELECT * FROM patients WHERE id=?', (patient_id,)).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail='Patient not found')
            return dict(row)

    @app.get('/api/patients/{patient_id}/appointments')
    def patient_appointments(patient_id: int):
        with connect() as conn:
            if not conn.execute('SELECT id FROM patients WHERE id=?', (patient_id,)).fetchone():
                raise HTTPException(status_code=404, detail='Patient not found')
            return [dict(row) for row in conn.execute('SELECT * FROM appointments WHERE patient_id=? ORDER BY id', (patient_id,))]

    @app.post('/api/appointments', status_code=201)
    def create_appointment(payload: AppointmentIn):
        if not payload.department.strip():
            raise HTTPException(status_code=422, detail='Department is required')
        with connect() as conn:
            patient = conn.execute('SELECT id FROM patients WHERE id=?', (payload.patient_id,)).fetchone()
            if patient is None:
                raise HTTPException(status_code=404, detail='Patient not found')
            cursor = conn.execute(
                'INSERT INTO appointments(patient_id, date, department) VALUES (?, ?, ?)',
                (payload.patient_id, payload.date, payload.department.strip()))
            return {'id': cursor.lastrowid, **payload.model_dump(), 'status': 'scheduled'}

    @app.get('/api/appointments')
    def list_appointments():
        with connect() as conn:
            return [dict(row) for row in conn.execute('SELECT * FROM appointments ORDER BY id')]

    @app.patch('/api/appointments/{appointment_id}/reschedule')
    def reschedule_appointment(appointment_id: int, new_date: str):
        try:
            Date.fromisoformat(new_date)
        except ValueError:
            raise HTTPException(status_code=422, detail='Invalid date')
        with connect() as conn:
            row = conn.execute('SELECT * FROM appointments WHERE id=?', (appointment_id,)).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail='Appointment not found')
            if row['status'] == 'cancelled':
                raise HTTPException(status_code=409, detail='Cannot reschedule cancelled appointment')
            conn.execute('UPDATE appointments SET date=? WHERE id=?', (new_date, appointment_id))
            return {'id': appointment_id, 'date': new_date, 'status': 'scheduled'}

    @app.patch('/api/appointments/{appointment_id}/cancel')
    def cancel_appointment(appointment_id: int):
        with connect() as conn:
            row = conn.execute('SELECT * FROM appointments WHERE id=?', (appointment_id,)).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail='Appointment not found')
            if row['status'] == 'cancelled':
                raise HTTPException(status_code=409, detail='Appointment already cancelled')
            conn.execute('UPDATE appointments SET status=? WHERE id=?', ('cancelled', appointment_id))
            return {'id': appointment_id, 'status': 'cancelled'}

    @app.get('/', response_class=HTMLResponse)
    def index():
        return '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>CareFlow QA Demo</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:36px auto;padding:0 18px;color:#162438;background:#f6f9fc}header{background:#123a61;color:white;padding:22px;border-radius:12px}main{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}.panel{background:white;border:1px solid #dce4ee;border-radius:12px;padding:20px}label{display:block;margin:12px 0 4px}input,select,button{font:inherit;padding:9px;border:1px solid #bdcbd9;border-radius:7px;width:100%;box-sizing:border-box}button{margin-top:18px;background:#0a5ea8;color:white;border:0;cursor:pointer}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid #ddd}#message{min-height:22px;color:#155724}@media(max-width:650px){main{grid-template-columns:1fr}}</style></head>
<body><header><h1>CareFlow QA Demo</h1><p>Fictional patients only · Appointment scheduling test application</p></header>
<p id="message" role="status"></p><main><section class="panel"><h2>Register patient</h2>
<form id="patient-form"><label for="name">Patient name</label><input id="name" required minlength="2" value="Alex Sample">
<label for="birth">Date of birth</label><input id="birth" type="date" required value="1995-03-12">
<button type="submit">Register patient</button></form></section>
<section class="panel"><h2>Schedule appointment</h2><form id="appointment-form">
<label for="patient">Patient</label><select id="patient" required></select>
<label for="date">Appointment date</label><input id="date" type="date" required value="2027-01-15">
<label for="department">Department</label><input id="department" required value="Cardiology">
<button type="submit">Schedule appointment</button></form></section></main>
<section class="panel" style="margin-top:18px"><h2>Appointments</h2><p id="metrics" aria-label="Operational metrics"></p><table><thead><tr><th>ID</th><th>Patient ID</th><th>Date</th><th>Department</th><th>Status</th><th>Action</th></tr></thead><tbody id="appointments"></tbody></table></section>
<script>
const msg=document.querySelector('#message');
async function request(path,options={}){const r=await fetch(path,{headers:{'Content-Type':'application/json'},...options});const data=await r.json();if(!r.ok)throw Error(data.detail||'Request failed');return data}
async function refresh(){const patients=await request('/api/patients');document.querySelector('#patient').innerHTML=patients.map(p=>`<option value="${p.id}">${p.id}: ${escapeHtml(p.name)}</option>`).join('');const a=await request('/api/appointments');document.querySelector('#appointments').innerHTML=a.map(x=>`<tr><td>${x.id}</td><td>${x.patient_id}</td><td>${x.date}</td><td>${escapeHtml(x.department)}</td><td>${x.status}</td><td>${x.status==='scheduled'?`<button type="button" data-cancel="${x.id}" aria-label="Cancel appointment ${x.id}">Cancel</button>`:'—'}</td></tr>`).join('');const m=await request('/api/metrics');document.querySelector('#metrics').textContent=`Patients: ${m.patients} · Scheduled: ${m.scheduled} · Cancelled: ${m.cancelled}`}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
document.querySelector('#appointments').addEventListener('click',async e=>{const id=e.target.dataset.cancel;if(!id)return;try{await request(`/api/appointments/${id}/cancel`,{method:'PATCH'});msg.textContent='Appointment cancelled successfully';await refresh()}catch(err){msg.textContent=err.message}});
document.querySelector('#patient-form').addEventListener('submit',async e=>{e.preventDefault();try{await request('/api/patients',{method:'POST',body:JSON.stringify({name:document.querySelector('#name').value,birth_date:document.querySelector('#birth').value})});msg.textContent='Patient registered successfully';await refresh()}catch(err){msg.textContent=err.message}});
document.querySelector('#appointment-form').addEventListener('submit',async e=>{e.preventDefault();try{await request('/api/appointments',{method:'POST',body:JSON.stringify({patient_id:Number(document.querySelector('#patient').value),date:document.querySelector('#date').value,department:document.querySelector('#department').value})});msg.textContent='Appointment scheduled successfully';await refresh()}catch(err){msg.textContent=err.message}});refresh();
</script></body></html>'''
    return app

app = create_app()
