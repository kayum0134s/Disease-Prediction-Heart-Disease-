/* ============================================================
   CardioPredict — API Client
   Base URL, fetch wrappers, error handling
   ============================================================ */

const API_BASE = 'http://localhost:5000/api';

async function _fetch(method, path, body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  try {
    const res  = await fetch(`${API_BASE}${path}`, opts);
    const data = await res.json();
    if (!data.success && res.status !== 200) {
      throw new Error(data.error || `HTTP ${res.status}`);
    }
    return data;
  } catch (err) {
    if (err.name === 'TypeError') {
      throw new Error('Cannot connect to CardioPredict server. Make sure run.py is running.');
    }
    throw err;
  }
}

const API = {
  health:           ()       => _fetch('GET',  '/health'),
  predict:          (data)   => _fetch('POST', '/predict', data),
  getAccuracy:      ()       => _fetch('GET',  '/models/accuracy'),
  getConfusion:     ()       => _fetch('GET',  '/models/confusion'),
  getFeatureImportance: ()   => _fetch('GET',  '/models/feature-importance'),
  getPatients:      ()       => _fetch('GET',  '/patients'),
  savePatient:      (data)   => _fetch('POST', '/patients', data),
  trainModels:      ()       => _fetch('POST', '/train'),
  reportUrl:        (id)     => `${API_BASE}/report/${id}`,
};

window.API = API;
