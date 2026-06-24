<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>SOC Alert Triage Dashboard</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0d1117; color: #e6edf3; }
  header { background: #161b22; border-bottom: 1px solid #30363d; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; }
  header h1 { font-size: 1.1rem; color: #58a6ff; }
  .stats-bar { display: flex; gap: 24px; background: #161b22; padding: 10px 24px; border-bottom: 1px solid #30363d; }
  .stat { font-size: 0.8rem; color: #8b949e; }
  .stat span { color: #e6edf3; font-weight: bold; }
  .main { display: flex; }
  .sidebar { width: 200px; background: #161b22; border-right: 1px solid #30363d; padding: 16px; }
  .sidebar h3 { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; margin-bottom: 12px; }
  .filter-btn { display: block; width: 100%; text-align: left; background: none; border: none; color: #e6edf3; padding: 6px 8px; border-radius: 4px; cursor: pointer; font-size: 0.85rem; margin-bottom: 4px; }
  .filter-btn:hover, .filter-btn.active { background: #21262d; }
  .content { flex: 1; padding: 16px; }
  table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  th { background: #21262d; padding: 8px 12px; text-align: left; color: #8b949e; font-weight: 600; border-bottom: 1px solid #30363d; }
  td { padding: 10px 12px; border-bottom: 1px solid #21262d; vertical-align: middle; }
  tr:hover td { background: #161b22; cursor: pointer; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 600; }
  .CRITICAL { background: #3d1a1a; color: #f85149; }
  .HIGH     { background: #3d2b1a; color: #fb8f44; }
  .MEDIUM   { background: #3d3a1a; color: #e3b341; }
  .LOW      { background: #1a3d2b; color: #56d364; }
  .status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; background: #21262d; color: #8b949e; }
  .status-badge.New { color: #58a6ff; }
  .status-badge.Investigating { color: #e3b341; }
  .status-badge.Closed { color: #56d364; }
</style>
</head>
<body>
<header>
  <h1>🛡️ SOC Alert Triage Dashboard</h1>
  <div style="font-size:0.8rem;color:#8b949e;">Analyst: J. Smith &nbsp;|&nbsp; Shift: Day &nbsp;|&nbsp; <span id="clock"></span></div>
</header>
<div class="stats-bar">
  <div class="stat">Open Alerts: <span id="open-count">—</span></div>
  <div class="stat">Critical: <span id="crit-count" style="color:#f85149">—</span></div>
  <div class="stat">MTTD (avg): <span>4.2 min</span></div>
  <div class="stat">MTTR (avg): <span>22 min</span></div>
  <div class="stat">Closed Today: <span>31</span></div>
</div>
<div class="main">
  <div class="sidebar">
    <h3>Filter</h3>
    <button class="filter-btn active" onclick="filterAlerts('ALL')">All Alerts</button>
    <button class="filter-btn" onclick="filterAlerts('CRITICAL')">🔴 Critical</button>
    <button class="filter-btn" onclick="filterAlerts('HIGH')">🟠 High</button>
    <button class="filter-btn" onclick="filterAlerts('MEDIUM')">🟡 Medium</button>
    <button class="filter-btn" onclick="filterAlerts('LOW')">🟢 Low</button>
    <br/>
    <h3>Status</h3>
    <button class="filter-btn" onclick="filterStatus('New')">New</button>
    <button class="filter-btn" onclick="filterStatus('Investigating')">Investigating</button>
    <button class="filter-btn" onclick="filterStatus('Closed')">Closed</button>
  </div>
  <div class="content">
    <table>
      <thead>
        <tr>
          <th>ID</th><th>Time</th><th>Severity</th><th>Alert Name</th><th>Source IP</th><th>Status</th><th>Assigned</th>
        </tr>
      </thead>
      <tbody id="alert-table"></tbody>
    </table>
  </div>
</div>
<script>
const alerts = [
  { id:"SOC-001", time:"08:02", sev:"CRITICAL", name:"Ransomware File Encryption Detected",  src:"10.0.1.55",    status:"Investigating", analyst:"J. Smith" },
  { id:"SOC-002", time:"08:14", sev:"HIGH",     name:"Brute Force SSH — 47 Failures",        src:"45.77.65.211", status:"New",           analyst:"—" },
  { id:"SOC-003", time:"08:21", sev:"HIGH",     name:"Lateral Movement — SMB Sweep",         src:"10.0.1.55",    status:"Investigating", analyst:"K. Patel" },
  { id:"SOC-004", time:"08:35", sev:"CRITICAL", name:"Data Exfiltration — 2.4 GB Outbound",  src:"10.0.2.100",   status:"New",           analyst:"—" },
  { id:"SOC-005", time:"08:40", sev:"MEDIUM",   name:"Suspicious PowerShell Execution",       src:"10.0.1.22",    status:"New",           analyst:"—" },
  { id:"SOC-006", time:"08:55", sev:"LOW",      name:"Port Scan Detected — 10 Ports",        src:"192.168.5.44", status:"Closed",        analyst:"J. Smith" },
  { id:"SOC-007", time:"09:05", sev:"HIGH",     name:"Phishing Email — 38 Recipients",       src:"External",     status:"Investigating", analyst:"M. Torres" },
  { id:"SOC-008", time:"09:11", sev:"MEDIUM",   name:"Unauthorized S3 Bucket Access",        src:"52.31.10.4",   status:"New",           analyst:"—" },
  { id:"SOC-009", time:"09:22", sev:"CRITICAL", name:"C2 Beacon — Cobalt Strike Detected",   src:"10.0.3.77",    status:"New",           analyst:"—" },
  { id:"SOC-010", time:"09:40", sev:"LOW",      name:"After-Hours Login — Admin Account",    src:"10.0.0.5",     status:"Closed",        analyst:"K. Patel" },
];

let currentFilter = "ALL";

function renderTable(data) {
  const tbody = document.getElementById("alert-table");
  tbody.innerHTML = data.map(a => `
    <tr>
      <td style="color:#8b949e">${a.id}</td>
      <td>${a.time}</td>
      <td><span class="badge ${a.sev}">${a.sev}</span></td>
      <td>${a.name}</td>
      <td style="font-family:monospace;font-size:0.8rem">${a.src}</td>
      <td><span class="status-badge ${a.status}">${a.status}</span></td>
      <td style="color:#8b949e">${a.analyst}</td>
    </tr>`).join("");
  document.getElementById("open-count").textContent = data.filter(a => a.status !== "Closed").length;
  document.getElementById("crit-count").textContent = data.filter(a => a.sev === "CRITICAL" && a.status !== "Closed").length;
}

function filterAlerts(sev) {
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");
  currentFilter = sev;
  const filtered = sev === "ALL" ? alerts : alerts.filter(a => a.sev === sev);
  renderTable(filtered);
}

function filterStatus(status) {
  renderTable(alerts.filter(a => a.status === status));
}

function tick() {
  document.getElementById("clock").textContent = new Date().toLocaleTimeString();
}

renderTable(alerts);
tick();
setInterval(tick, 1000);
</script>
</body>
</html>
