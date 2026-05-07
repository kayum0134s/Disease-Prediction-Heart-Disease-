/* ============================================================
   CardioPredict — Model Comparison Charts (Chart.js)
   ============================================================ */

const METRIC_LABELS = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUC'];
const METRIC_KEYS   = ['accuracy', 'precision', 'recall', 'f1', 'auc'];

const MODEL_COLORS = {
  'Logistic Regression': { bg: 'rgba(0,212,255,0.6)',  border: '#00d4ff' },
  'Random Forest':       { bg: 'rgba(0,255,136,0.6)',  border: '#00ff88' },
  'SVM':                 { bg: 'rgba(191,90,242,0.6)', border: '#bf5af2' },
};

let barChart = null;

async function loadComparison() {
  const loading = document.getElementById('comparison-loading');
  if (loading) loading.style.display = 'flex';

  try {
    const res = await API.getAccuracy();
    if (!res.success) throw new Error(res.error);
    renderComparison(res.data);
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    if (loading) loading.style.display = 'none';
  }

  // ROC curve image
  try {
    const fi = await API.getFeatureImportance();
    if (fi.success) {
      const rocImg = document.getElementById('roc-img');
      if (rocImg) rocImg.src = `data:image/png;base64,${fi.data.roc}`;
    }
  } catch {}
}

function renderComparison(metrics) {
  // Model cards
  const cardsEl = document.getElementById('model-cards');
  if (cardsEl) {
    cardsEl.innerHTML = '';
    let bestAcc = 0, bestName = '';
    for (const [name, m] of Object.entries(metrics)) {
      if (m.accuracy > bestAcc) { bestAcc = m.accuracy; bestName = name; }
    }
    for (const [name, m] of Object.entries(metrics)) {
      const isBest = name === bestName;
      const color  = MODEL_COLORS[name] || {};
      const card   = document.createElement('div');
      card.className = `model-card ${isBest ? 'best-model' : ''} hover-lift`;
      card.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between">
          <span class="model-name">${name}</span>
          ${isBest ? '<span class="badge badge-yellow">🏆 Best Model</span>' : ''}
        </div>
        <div class="divider"></div>
        ${METRIC_LABELS.map((label, i) => `
          <div class="metric-row">
            <span class="metric-label">${label}</span>
            <span class="metric-val" style="color:${color.border||'#00d4ff'}">${m[METRIC_KEYS[i]]}%</span>
          </div>
          <div class="progress-track"><div class="progress-fill" style="width:0%;background:${color.border||'#00d4ff'}"></div></div>
        `).join('')}
      `;
      cardsEl.appendChild(card);
      setTimeout(() => {
        card.querySelectorAll('.progress-fill').forEach((bar, i) => {
          bar.style.transition = `width 1.2s ${0.1*i}s ease`;
          bar.style.width = `${m[METRIC_KEYS[i]]}%`;
        });
      }, 200);
    }
    // Best banner
    const banner = document.getElementById('best-banner');
    if (banner) {
      banner.querySelector('.best-banner-text').textContent = `${bestName} is the Best Performing Model`;
      banner.querySelector('.best-banner-sub').textContent  = `Accuracy: ${bestAcc}% — Used as Final Prediction Engine`;
      banner.style.display = 'flex';
    }
  }

  // Grouped bar chart
  const ctx = document.getElementById('comparison-chart');
  if (!ctx) return;
  if (barChart) barChart.destroy();

  const datasets = Object.entries(metrics).map(([name, m]) => ({
    label:           name,
    data:            METRIC_KEYS.map(k => m[k]),
    backgroundColor: MODEL_COLORS[name]?.bg     || 'rgba(0,212,255,0.5)',
    borderColor:     MODEL_COLORS[name]?.border  || '#00d4ff',
    borderWidth:     1.5,
    borderRadius:    6,
  }));

  barChart = new Chart(ctx, {
    type: 'bar',
    data: { labels: METRIC_LABELS, datasets },
    options: {
      responsive: true,
      animation: { duration: 1000, easing: 'easeOutQuart' },
      plugins: {
        legend: { labels: { color: '#ccd6f6', font: { family: 'Inter', size: 12 } } },
        tooltip: { backgroundColor: '#0d1b3e', borderColor: '#00d4ff', borderWidth: 1 },
      },
      scales: {
        x: { ticks: { color: '#8892b0' }, grid: { color: 'rgba(0,212,255,0.06)' } },
        y: {
          min: 50, max: 100,
          ticks: { color: '#8892b0', callback: v => `${v}%` },
          grid:  { color: 'rgba(0,212,255,0.06)' },
        },
      },
    },
  });
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('comparison-chart')) loadComparison();
});
