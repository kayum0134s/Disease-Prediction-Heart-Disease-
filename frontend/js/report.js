/* ============================================================
   CardioPredict — Report & Patient History
   ============================================================ */

let allPatients = [];

async function loadPatients() {
  const loading = document.getElementById('patients-loading');
  const tbody   = document.getElementById('patients-tbody');
  if (!tbody) return;

  if (loading) loading.style.display = 'flex';
  try {
    const res = await API.getPatients();
    if (!res.success) throw new Error(res.error);
    allPatients = res.data;
    renderTable(allPatients);
    updateStats(allPatients);
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    if (loading) loading.style.display = 'none';
  }
}

function renderTable(patients) {
  const tbody = document.getElementById('patients-tbody');
  if (!tbody) return;
  if (patients.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8"><div class="empty-state"><div class="empty-icon">📋</div><p class="empty-text">No patient records yet.<br>Run a prediction on the Dashboard to get started.</p></div></td></tr>`;
    return;
  }
  tbody.innerHTML = patients.map(p => `
    <tr>
      <td><span style="font-family:var(--font-display);color:var(--neon-blue);font-size:0.85rem">CP-${String(p.id).padStart(4,'0')}</span></td>
      <td><span style="font-weight:600">${p.name}</span></td>
      <td>${p.age} yrs</td>
      <td>${p.sex}</td>
      <td>
        <span class="badge ${p.prediction===1?'badge-red':'badge-green'}">
          ${p.prediction===1?'Positive':'Negative'}
        </span>
      </td>
      <td>
        <span style="font-family:var(--font-display);font-weight:700;color:${getRiskColorFromLabel(p.risk_label)}">
          ${p.risk_score}%
        </span>
      </td>
      <td><span class="badge ${getRiskBadgeClass(p.risk_label)}">${p.risk_label}</span></td>
      <td>${p.timestamp}</td>
      <td>
        <a href="${API.reportUrl(p.id)}" target="_blank" class="btn btn-sm btn-primary">
          📄 PDF
        </a>
      </td>
    </tr>
  `).join('');
}

function getRiskColorFromLabel(label) {
  if (!label) return '#8892b0';
  const l = label.toLowerCase();
  if (l.includes('low'))      return '#00ff88';
  if (l.includes('moderate')) return '#ffd60a';
  if (l.includes('high'))     return '#ff9500';
  if (l.includes('critical')) return '#ff2d55';
  return '#8892b0';
}

function getRiskBadgeClass(label) {
  if (!label) return 'badge-blue';
  const l = label.toLowerCase();
  if (l.includes('low'))      return 'badge-green';
  if (l.includes('moderate')) return 'badge-yellow';
  if (l.includes('high'))     return 'badge-orange';
  if (l.includes('critical')) return 'badge-red';
  return 'badge-blue';
}

function updateStats(patients) {
  const total    = patients.length;
  const positive = patients.filter(p => p.prediction === 1).length;
  const avgRisk  = total ? (patients.reduce((s,p) => s + p.risk_score, 0) / total).toFixed(1) : 0;

  const totalEl = document.getElementById('stat-total');
  const posEl   = document.getElementById('stat-positive');
  const avgEl   = document.getElementById('stat-avg-risk');

  if (totalEl) animateNumber(totalEl, total, 800, 0);
  if (posEl)   animateNumber(posEl, positive, 800, 0);
  if (avgEl)   animateNumber(avgEl, avgRisk, 1000, 1, '%');
}

// ── Search filter ──────────────────────────────────────────
const searchInput = document.getElementById('search-input');
if (searchInput) {
  searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase();
    const filtered = allPatients.filter(p =>
      p.name.toLowerCase().includes(q) ||
      String(p.id).includes(q) ||
      (p.risk_label || '').toLowerCase().includes(q)
    );
    renderTable(filtered);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('patients-tbody')) loadPatients();
});
