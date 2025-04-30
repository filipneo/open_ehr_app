import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [patients, setPatients] = useState([]);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [sex, setSex] = useState('');
  const [identifier, setIdentifier] = useState('');

  const fetchPatients = async () => {
    const res = await axios.get('http://localhost:8000/patients');
    setPatients(res.data);
  };

  const addPatient = async (e) => {
    e.preventDefault();
    await axios.post('http://localhost:8000/patients', {
      first_name: firstName,
      last_name: lastName,
      sex,
      identifier
    });
    setFirstName('');
    setLastName('');
    setSex('');
    setIdentifier('');
    fetchPatients();
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Patients</h1>
      <form onSubmit={addPatient}>
        <input placeholder="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} /> <br/>
        <input placeholder="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} /> <br/>
        <input placeholder="Sex" value={sex} onChange={e => setSex(e.target.value)} /> <br/>
        <input placeholder="Identifier" value={identifier} onChange={e => setIdentifier(e.target.value)} /> <br/>
        <button type="submit">Add Patient</button>
      </form>

      <h2>Existing Patients</h2>
      <ul>
        {patients.map(p => (
          <li key={p.id}>
            {p.first_name} {p.last_name} - {p.sex} - ID: {p.id}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
