// JS to fetch data for Chart.js and to request downloads from an API endpoint.
document.addEventListener('DOMContentLoaded', function () {
  const downloadBtn = document.getElementById('downloadBtn');
  const startInput = document.getElementById('start');
  const endInput = document.getElementById('end');
  const formatSelect = document.getElementById('format');
  const canvas = document.getElementById('mainChart');
  const ctx = canvas ? canvas.getContext('2d') : null;

  let chart = null;

  async function fetchAndPlot() {
    const start = startInput.value;
    const end = endInput.value;
    if (!start || !end || !ctx) return;
    const url = `${API_BASE}/timeseries?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const json = await res.json();
      const labels = json.labels || [];
      const data = json.amplitudes || [];

      if (chart) chart.destroy();
      chart = new Chart(ctx, {
        type: 'line',
        data: { labels: labels, datasets: [{ label: 'Amplitud', data: data, borderColor: 'blue', tension: 0.1 }] },
        options: { responsive: true }
      });
    } catch (err) {
      console.warn('No se pudieron obtener datos para la gráfica:', err);
    }
  }

  if (downloadBtn) {
    downloadBtn.addEventListener('click', async function () {
      const start = startInput.value;
      const end = endInput.value;
      const format = formatSelect.value;
      if (!start || !end) {
        alert('Seleccione fecha inicio y fecha fin');
        return;
      }
      const url = `${API_BASE}/export?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}&format=${encodeURIComponent(format)}`;
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const blob = await res.blob();
        let filename = 'datos.' + (format === 'xlsx' ? 'xlsx' : 'csv');
        const disposition = res.headers.get('content-disposition') || '';
        const matches = /filename="?([^";]+)"?/.exec(disposition);
        if (matches) filename = matches[1];
        const link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        alert('Error descargando los datos: ' + err.message);
      }
    });
  }

  if (startInput && endInput) {
    [startInput, endInput].forEach(el => el.addEventListener('change', fetchAndPlot));
  }
});
