/* ============================================================
   CardioPredict — Analytics Page JS
   Confusion matrices · Feature importance · Dataset distributions
   ============================================================ */

async function loadAnalytics() {
  const loading = document.getElementById('analytics-loading');
  if (loading) loading.style.display = 'flex';

  try {
    const [confRes, fiRes] = await Promise.all([
      API.getConfusion(),
      API.getFeatureImportance(),
    ]);

    if (confRes.success) renderConfusionMatrices(confRes.data);
    if (fiRes.success)   renderFeatureImportance(fiRes.data);
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    if (loading) loading.style.display = 'none';
  }
}

function renderConfusionMatrices(data) {
  const models = ['Logistic Regression', 'Random Forest', 'SVM'];
  models.forEach(name => {
    const id  = `cm-${name.toLowerCase().replace(/\s+/g,'-')}`;
    const img = document.getElementById(id);
    if (img && data[name]) {
      img.src = `data:image/png;base64,${data[name]}`;
      img.style.opacity = '0';
      img.onload = () => { img.style.transition='opacity 0.5s'; img.style.opacity='1'; };
    }
  });
}

function renderFeatureImportance(data) {
  const fiImg = document.getElementById('fi-img');
  if (fiImg && data.image) {
    fiImg.src = `data:image/png;base64,${data.image}`;
  }
  const rocImg = document.getElementById('roc-analytics-img');
  if (rocImg && data.roc) {
    rocImg.src = `data:image/png;base64,${data.roc}`;
  }
}

// Dataset distribution charts (hardcoded illustrative data)
function renderDistributions() {
  const ageCtx = document.getElementById('age-dist');
  if (ageCtx) {
    new Chart(ageCtx, {
      type: 'bar',
      data: {
        labels: ['29-39','40-49','50-59','60-69','70-77'],
        datasets: [{
          label: 'Patients',
          data: [82, 238, 356, 254, 70],
          backgroundColor: 'rgba(0,212,255,0.5)',
          borderColor: '#00d4ff',
          borderWidth: 1.5,
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false }, tooltip: { backgroundColor: '#0d1b3e', borderColor: '#00d4ff', borderWidth: 1 } },
        scales: {
          x: { ticks: { color: '#8892b0' }, grid: { color: 'rgba(0,212,255,0.05)' } },
          y: { ticks: { color: '#8892b0' }, grid: { color: 'rgba(0,212,255,0.05)' } },
        },
      },
    });
  }

  const sexCtx = document.getElementById('sex-dist');
  if (sexCtx) {
    new Chart(sexCtx, {
      type: 'doughnut',
      data: {
        labels: ['Male', 'Female'],
        datasets: [{
          data: [680, 320],
          backgroundColor: ['rgba(0,212,255,0.6)', 'rgba(255,45,85,0.6)'],
          borderColor: ['#00d4ff', '#ff2d55'],
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { labels: { color: '#ccd6f6', font: { family: 'Inter', size: 12 } } },
          tooltip: { backgroundColor: '#0d1b3e', borderColor: '#00d4ff', borderWidth: 1 },
        },
        cutout: '65%',
      },
    });
  }

  const cpCtx = document.getElementById('cp-dist');
  if (cpCtx) {
    new Chart(cpCtx, {
      type: 'bar',
      data: {
        labels: ['Typical Angina', 'Atypical Angina', 'Non-Anginal', 'Asymptomatic'],
        datasets: [{
          label: 'Count',
          data: [80, 160, 280, 480],
          backgroundColor: ['rgba(0,255,136,0.5)','rgba(0,212,255,0.5)','rgba(191,90,242,0.5)','rgba(255,45,85,0.5)'],
          borderColor:     ['#00ff88','#00d4ff','#bf5af2','#ff2d55'],
          borderWidth: 1.5, borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false }, tooltip: { backgroundColor: '#0d1b3e', borderColor: '#00d4ff', borderWidth: 1 } },
        scales: {
          x: { ticks: { color: '#8892b0', maxRotation: 30 }, grid: { color: 'rgba(0,212,255,0.05)' } },
          y: { ticks: { color: '#8892b0' }, grid: { color: 'rgba(0,212,255,0.05)' } },
        },
      },
    });
  }

  const targetCtx = document.getElementById('target-dist');
  if (targetCtx) {
    new Chart(targetCtx, {
      type: 'doughnut',
      data: {
        labels: ['No Disease', 'Heart Disease'],
        datasets: [{
          data: [460, 540],
          backgroundColor: ['rgba(0,255,136,0.6)', 'rgba(255,45,85,0.6)'],
          borderColor: ['#00ff88', '#ff2d55'],
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { labels: { color: '#ccd6f6', font: { family: 'Inter', size: 12 } } },
          tooltip: { backgroundColor: '#0d1b3e', borderColor: '#00d4ff', borderWidth: 1 },
        },
        cutout: '65%',
      },
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('fi-img')) {
    loadAnalytics();
    renderDistributions();
  }
});
