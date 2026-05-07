/* ============================================================
   CardioPredict — Navigation & Toast Utilities
   ============================================================ */

// ── Active nav link ────────────────────────────────────────
(function setActiveNav() {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page || (page === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
})();

// ── Toast notifications ────────────────────────────────────
function showToast(msg, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3100);
}

// ── Animate numbers counting up ───────────────────────────
function animateNumber(el, target, duration = 1200, decimals = 1, suffix = '') {
  const start = performance.now();
  const from  = 0;
  function tick(now) {
    const pct = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - pct, 3);
    const val  = from + (target - from) * ease;
    el.textContent = val.toFixed(decimals) + suffix;
    if (pct < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ── Risk color helper ──────────────────────────────────────
function getRiskColor(riskPct) {
  if (riskPct < 30)  return '#00ff88';
  if (riskPct < 60)  return '#ffd60a';
  if (riskPct < 80)  return '#ff9500';
  return '#ff2d55';
}

// ── Gauge update ───────────────────────────────────────────
function updateGauge(svgId, valueElId, pct) {
  const arc   = document.getElementById(svgId);
  const label = document.getElementById(valueElId);
  if (!arc || !label) return;

  const r = 90;
  const circumference = Math.PI * r;   // half-circle: πr
  const offset = circumference * (1 - pct / 100);

  arc.style.strokeDasharray  = circumference;
  arc.style.strokeDashoffset = offset;
  arc.style.stroke = getRiskColor(pct);

  animateNumber(label, pct, 1400, 1, '%');
}

// ── Progress bar fill ──────────────────────────────────────
function fillProgressBar(barEl, pct, colorClass = 'progress-blue') {
  if (!barEl) return;
  barEl.style.width = '0%';
  barEl.className   = `progress-fill ${colorClass}`;
  requestAnimationFrame(() => {
    barEl.style.transition = 'width 1.2s cubic-bezier(0.4,0,0.2,1)';
    barEl.style.width      = `${pct}%`;
  });
}

// ── Server status check ────────────────────────────────────
async function checkServerStatus() {
  const dot  = document.getElementById('status-dot');
  const text = document.getElementById('status-text');
  try {
    await API.health();
    if (dot)  { dot.className  = 'dot dot-green'; }
    if (text) { text.textContent = 'System Online'; }
  } catch {
    if (dot)  { dot.className  = 'dot dot-red'; }
    if (text) { text.textContent = 'Server Offline'; }
  }
}

window.showToast         = showToast;
window.animateNumber     = animateNumber;
window.getRiskColor      = getRiskColor;
window.updateGauge       = updateGauge;
window.fillProgressBar   = fillProgressBar;
window.checkServerStatus = checkServerStatus;

document.addEventListener('DOMContentLoaded', () => {
  checkServerStatus();
  // Page entrance animation
  document.body.classList.add('page-enter');
});
