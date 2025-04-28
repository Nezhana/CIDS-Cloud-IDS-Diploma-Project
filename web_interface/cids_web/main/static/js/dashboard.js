// dashboard.js

// document.addEventListener("DOMContentLoaded", () => {
//     // Event Statistics Chart
//     const ctx = document.getElementById("eventChart").getContext("2d");
//     fetch("/dashboard/api/event-data/")
//       .then(response => response.json())
//       .then(chartData => {
//         const ctx = document.getElementById("eventChart").getContext("2d");
//         new Chart(ctx, {
//           type: "line",
//           data: {
//             labels: chartData.labels,
//             datasets: [{
//               label: "Events",
//               data: chartData.values,
//               borderColor: "#00d9d9",
//               fill: false,
//               tension: 0.4
//             }]
//           },
          // options: {
          //   scales: {
          //     x: { ticks: { color: '#c2f2f2' }, grid: { color: '#1a2f33' } },
          //     y: { ticks: { color: '#c2f2f2' }, grid: { color: '#1a2f33' } }
          //   },
          //   plugins: {
          //     legend: { labels: { color: '#c2f2f2' } }
          //   }
          // }
//         });
//       });
  
//     // Last Log Data
//     const logs = [
//       "22-04-2025 12:53:41 | 168.132.14.148 | Malicious IP Address",
//       "22-04-2025 12:53:41 | 164.112.14.189 | Malicious IP Address",
//       "22-04-2025 12:53:41 | 112.132.11.56 | Malicious IP Address",
//       "22-04-2025 12:53:41 | 176.13.12.113 | GET key_name.txt",
//       "22-04-2025 12:53:41 | 176.13.12.113 | GET key_name.txt",
//       "22-04-2025 12:53:41 | 176.13.12.113 | GET key_name.txt",
//       "22-04-2025 12:53:41 | 111.111.11.111 | Malicious IP Address"
//     ];
  
//     const logList = document.getElementById("logList");
//     logs.forEach(log => {
//       const li = document.createElement("li");
//       li.textContent = log;
//       logList.appendChild(li);
//     });
  
//     // Top Requests
//     const requests = [
//       { ip: "176.13.12.113", count: 5 },
//       { ip: "164.112.14.189", count: 4 },
//       { ip: "111.111.11.111", count: 3 },
//       { ip: "112.132.11.56", count: 2 }
//     ];
  
//     const topRequests = document.getElementById("topRequests");
//     requests.forEach(req => {
//       const li = document.createElement("li");
//       li.textContent = `${req.ip} - ${req.count} requests`;
//       topRequests.appendChild(li);
//     });
  
//     // Sent Alerts
//     const alerts = [
//       "17/03/2025 11:20:00 - Malicious IP address detected: 112.132.11.56",
//       "16/03/2025 12:20:00 - Malicious IP address detected: 112.132.11.56",
//       "16/03/2025 12:40:00 - DDoS Warning: 111.111.11.111 exceeded requests",
//       "14/03/2025 16:44:00 - Access Denied: Unknown user agent"
//     ];
  
//     const alertsList = document.getElementById("alertsList");
//     alerts.forEach(alert => {
//       const li = document.createElement("li");
//       li.textContent = alert;
//       alertsList.appendChild(li);
//     });
//   });
  

// dashboard.js

// let chartInstance;

// function updateChart() {
//   fetch("/dashboard/api/event-data/")
//     .then(response => response.json())
//     .then(chartData => {
//       if (chartInstance) {
//         chartInstance.data.labels = chartData.labels;
//         chartInstance.data.datasets[0].data = chartData.values;
//         chartInstance.update();
//       } else {
//         const ctx = document.getElementById("eventChart").getContext("2d");
//         chartInstance = new Chart(ctx, {
//           type: "line",
//           data: {
//             labels: chartData.labels,
//             datasets: [{
//               label: "Events",
//               data: chartData.values,
//               borderColor: "#00d9d9",
//               fill: false,
//               tension: 0.4
//             }]
//           },
//           options: {
//             scales: {
//               x: { ticks: { color: '#c2f2f2' }, grid: { color: '#1a2f33' } },
//               y: { ticks: { color: '#c2f2f2' }, grid: { color: '#1a2f33' } }
//             },
//             plugins: {
//               legend: { labels: { color: '#c2f2f2' } }
//             }
//           }
//         });
//       }
//     });
// }

// function updateLogs() {
//   fetch("/dashboard/api/logs/")
//     .then(response => response.json())
//     .then(data => {
//       const logList = document.getElementById("logList");
//       logList.innerHTML = "";
//       data.logs.forEach(item => {
//         const li = document.createElement("li");
//         li.textContent = item;
//         logList.appendChild(li);
//       });
//     });
// }

// function updateTopRequests() {
//   fetch("/dashboard/api/top-requests/")
//     .then(response => response.json())
//     .then(data => {
//       const requestList = document.getElementById("topRequests");
//       requestList.innerHTML = "";
//       data.requests.forEach(req => {
//         const li = document.createElement("li");
//         li.textContent = `${req.ip} | ${req.count} requests`;
//         requestList.appendChild(li);
//       });
//     });
// }

// function updateAlerts() {
//   fetch("/dashboard/api/alerts/")
//     .then(response => response.json())
//     .then(data => {
//       const alertsList = document.getElementById("alertsList");
//       alertsList.innerHTML = "";
//       data.alerts.forEach(alert => {
//         const li = document.createElement("li");
//         li.textContent = alert;
//         alertsList.appendChild(li);
//       });
//     });
// }

// // Initial load
// updateChart();
// updateLogs();
// updateTopRequests();
// updateAlerts();

// // Auto-refresh every 300 seconds
// setInterval(() => {
//   updateChart();
//   updateLogs();
//   updateTopRequests();
//   updateAlerts();
// }, 300000);





document.addEventListener('DOMContentLoaded', async function () {
  const chartLoader = document.getElementById('chart-loader');
  const logsLoader = document.getElementById('logs-loader');
  const requestsLoader = document.getElementById('requests-loader');
  const alertsLoader = document.getElementById('alerts-loader');

  try {
      // Показуємо лоадери
      chartLoader.style.display = 'block';
      logsLoader.style.display = 'block';
      requestsLoader.style.display = 'block';
      alertsLoader.style.display = 'block';

      // 1. Завантажити дані для графіку
      const chartResponse = await fetch('/dashboard/api/event-data/');
      const chartData = await chartResponse.json();
      renderChart(chartData);
      chartLoader.style.display = 'none';


      // 2. Завантажити логи
      const logsResponse = await fetch('/dashboard/api/logs/');
      const logsData = await logsResponse.json();
      renderLogs(logsData);
      logsLoader.style.display = 'none';

      // 3. Завантажити логи
      const requestsResponse = await fetch('/dashboard/api/top-requests/');
      const requestsData = await requestsResponse.json();
      renderTopRequests(requestsData);
      requestsLoader.style.display = 'none';


      // 4. Завантажити алерти
      const alertsResponse = await fetch('/dashboard/api/alerts/');
      const alertsData = await alertsResponse.json();
      renderAlerts(alertsData);
      alertsLoader.style.display = 'none';


  } catch (error) {
      console.error('Error loading dashboard data:', error);
  } finally {
      // Прибрати лоадери після завантаження
      alertsLoader.style.display = 'none';
  }
});

let chartInstance;

// Функції відображення даних
function renderChart(chartData) {
    if (chartInstance) {
      chartInstance.data.labels = chartData.labels;
      chartInstance.data.datasets[0].data = chartData.values;
      chartInstance.update();
    } else {
      const ctx = document.getElementById("eventChart").getContext("2d");
      chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: chartData.labels,
          datasets: [{
            label: "Events",
            data: chartData.values,
            borderColor: "#00d9d9",
            fill: false,
            tension: 0.4
          }]
        },
        options: {
          scales: {
            x: { ticks: { color: '#c2f2f2' }, grid: { color: '#1a2f33' } },
            y: { ticks: { color: '#c2f2f2' }, grid: { color: '#1a2f33' } }
          },
          plugins: {
            legend: { labels: { color: '#c2f2f2' } }
          }
        }
      });
    }
  console.log('Drawing chart...', chartData.labels, chartData.values);
}

function renderLogs(logs) {
  console.log(logs)
  // Тут має бути код для відображення логів на сторінці
  const logList = document.getElementById("logList");
  logList.innerHTML = "";
  Object.keys(logs['logs']).forEach(key => {
    console.log(`${key}: ${logs['logs'][key]}`);
    const li = document.createElement("li");
    li.textContent = logs['logs'][key];
    logList.appendChild(li);
  });
  console.log('Rendering logs...', logs);
}

function renderTopRequests(requests) {
  console.log(requests)
  // Відобразити топ IP адрес
  const requestList = document.getElementById("topRequests");
  requestList.innerHTML = "";
  for (const key in requests) {
    console.log(`${key}: ${requests[key]}`);
    requests[key].forEach(req => {
      const li = document.createElement("li");
      li.textContent = requests[key];
      requestList.appendChild(li);
    });
  }
  console.log('Rendering top requests...', requests);
}

function renderAlerts(alerts) {
  console.log(alerts)
  // Вивести сповіщення
  const alertsList = document.getElementById("alertsList");
  alertsList.innerHTML = "";
  Object.keys(alerts['alerts']).forEach(key => {
    // console.log(`${key}: ${alerts[key]}`);
    const li = document.createElement("li");
    li.textContent = alerts['alerts'][key];
    alertsList.appendChild(li);
  });
  // alerts.forEach(alert => {
  //   const li = document.createElement("li");
  //   li.textContent = alert;
  //   alertsList.appendChild(li);
  // })
  console.log('Rendering alerts...', alerts);
}






// document.addEventListener('DOMContentLoaded', function () {
//   loadDashboardData();
// });

// async function loadDashboardData() {
//   try {
//       await loadChart();
//       await loadLogs();
//       await loadAlerts();
//   } catch (error) {
//       console.error('Dashboard load error:', error);
//   }
// }

// async function loadChart() {
//   const response = await fetch('/dashboard/api/event-data/');
//   const data = await response.json();
//   console.log('Chart Data:', data);

//   const ctx = document.getElementById('eventChart').getContext('2d');
//   new Chart(ctx, {
//       type: 'line',
//       data: {
//           labels: data.labels,
//           datasets: [{
//               label: 'Events',
//               data: data.values,
//               borderColor: 'blue',
//               fill: false
//           }]
//       }
//   });
// }

// async function loadLogs() {
//   const response = await fetch('/dashboard/api/logs/');
//   const data = await response.json();
//   console.log('Logs:', data);

//   const logsContainer = document.getElementById('logList');
//   logsContainer.innerHTML = '';
//   data.logs.forEach(log => {
//       const p = document.createElement('p');
//       p.textContent = log;
//       logsContainer.appendChild(p);
//   });
// }

// async function loadAlerts() {
//   const response = await fetch('/dashboard/api/alerts/');
//   const data = await response.json();
//   console.log('Alerts:', data);

//   const alertsContainer = document.getElementById('alertsList');
//   alertsContainer.innerHTML = '';
//   data.alerts.forEach(alert => {
//       const p = document.createElement('p');
//       p.textContent = alert;
//       alertsContainer.appendChild(p);
//   });
// }
