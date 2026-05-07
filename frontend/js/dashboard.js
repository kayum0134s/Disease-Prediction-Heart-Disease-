/* ============================================================
   CardioPredict — Dashboard Prediction Logic
   ============================================================ */

const form        = document.getElementById('prediction-form');
const submitBtn   = document.getElementById('submit-btn');
const resultsArea = document.getElementById('results-area');
const placeholder = document.getElementById('result-placeholder');

// ── Form submit ────────────────────────────────────────────
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await runPrediction();
  });
}

async function runPrediction() {
  const payload = buildPayload();
  if (!payload) return;

  setLoading(true);

  try {
    const res = await API.predict(payload);
    if (!res.success) throw new Error(res.error);
    const d = res.data;
    renderResults(d);
    showToast('Prediction complete', 'success');
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    setLoading(false);
  }
}

function buildPayload() {
  const fd   = new FormData(form);
  const name = document.getElementById('patient-name').value.trim() || 'Anonymous';
  const payload = { name };

  const fields = ['age','sex','cp','trestbps','chol','fbs','restecg',
                  'thalach','exang','oldpeak','slope','ca','thal'];
  for (const f of fields) {
    const val = fd.get(f);
    if (val === null || val === '') {
      showToast(`Please fill in all required fields.`, 'error');
      return null;
    }
    payload[f] = isNaN(val) ? val : Number(val);
  }
  return payload;
}

function setLoading(on) {
  if (!submitBtn) return;
  submitBtn.disabled = on;
  submitBtn.classList.toggle('loading', on);
  const txt = submitBtn.querySelector('.btn-text');
  if (txt) txt.textContent = on ? 'Analyzing...' : 'Run Prediction';
}

// ── Render results ─────────────────────────────────────────
function renderResults(d) {
  if (placeholder) placeholder.style.display = 'none';
  if (resultsArea) resultsArea.style.display = 'flex';

  // Gauge
  setTimeout(() => updateGauge('gauge-arc', 'gauge-value', d.risk_score), 100);

  // Risk label badge
  const riskLabel = document.getElementById('risk-label');
  if (riskLabel) {
    riskLabel.textContent = d.risk_label;
    riskLabel.style.color = d.risk_color;
  }

  // Result panel
  const panel = document.getElementById('result-panel');
  if (panel) {
    panel.className = `result-panel result-reveal ${d.prediction === 1 ? 'positive' : 'negative'}`;
    const icon  = panel.querySelector('.result-icon');
    const title = panel.querySelector('.result-title');
    const sub   = panel.querySelector('.result-sub');
    if (icon)  icon.textContent  = d.prediction === 1 ? '⚠️' : '✅';
    if (title) title.textContent = d.prediction_label;
    if (sub)   sub.textContent   = `Confidence: ${d.per_model['Random Forest'].probability}% (Random Forest)`;
  }

  // Model breakdown
  const modelColors = {
    'Logistic Regression': '#00d4ff',
    'Random Forest':       '#00ff88',
    'SVM':                 '#bf5af2',
  };
  const breakdownEl = document.getElementById('model-breakdown');
  if (breakdownEl) {
    breakdownEl.innerHTML = '';
    for (const [name, m] of Object.entries(d.per_model)) {
      const row  = document.createElement('div');
      row.className = 'model-row';
      const color = modelColors[name] || '#00d4ff';
      row.innerHTML = `
        <span class="model-row-name">${name}</span>
        <div class="model-row-bar">
          <div class="model-row-fill" style="width:0%;background:${color}"></div>
        </div>
        <span class="model-row-prob" style="color:${color}">${m.probability}%</span>
        <span class="badge ${m.prediction===1?'badge-red':'badge-green'}">${m.prediction===1?'Positive':'Negative'}</span>
      `;
      breakdownEl.appendChild(row);
      // animate bar
      setTimeout(() => {
        const fill = row.querySelector('.model-row-fill');
        if (fill) fill.style.cssText += `transition:width 1s ease;width:${m.probability}%`;
      }, 200);
    }
  }

  // Recommendations
  const recList = document.getElementById('rec-list');
  if (recList) {
    recList.innerHTML = d.recommendations.map(r =>
      `<li class="rec-item">${r}</li>`
    ).join('');
  }

  // Best model badge
  const bestEl = document.getElementById('best-model');
  if (bestEl) bestEl.textContent = d.best_model;

  // Save buttons
  const pdfBtn = document.getElementById('download-pdf-btn');
  if (pdfBtn && d.patient_id) {
    pdfBtn.href    = API.reportUrl(d.patient_id);
    pdfBtn.target  = '_blank';
    pdfBtn.style.display = 'inline-flex';
  }
}

// ── Range sliders live display ─────────────────────────────
document.querySelectorAll('input[type="range"]').forEach(input => {
  const display = document.getElementById(`${input.id}-val`);
  if (display) {
    display.textContent = input.value;
    input.addEventListener('input', () => { display.textContent = input.value; });
  }
});
