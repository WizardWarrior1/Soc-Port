# 🖥️ SIEM Alert Triage Dashboard

An interactive, browser-based SOC alert triage dashboard. Displays mock SIEM alerts with filtering, prioritization, and an analyst workflow (Acknowledge → Investigate → Close). Built with vanilla HTML/CSS/JS — no backend required.

## Features

- Real-time alert queue with mock data feed
- Severity filtering (Critical / High / Medium / Low)
- Alert status workflow: `New → Acknowledged → Investigating → Closed`
- Analyst assignment panel
- Alert detail modal with IOCs and recommended actions
- Alert statistics bar (MTTD, queue depth, open count)

## Tech Stack

- HTML5 / CSS3 / Vanilla JavaScript
- No frameworks or external dependencies
- Fully offline-capable

## Setup

```bash
git clone https://github.com/yourusername/siem-alert-triage-dashboard.git
cd siem-alert-triage-dashboard

# Just open in browser — no server needed
open index.html
```

## Screenshots

The dashboard includes:
- Alert table with color-coded severity badges
- Sidebar with alert breakdown by type
- Click-through to full alert detail modal
- Analyst notes field per alert

## Project Structure

```
siem-alert-triage-dashboard/
├── index.html
├── css/
│   └── dashboard.css
├── js/
│   ├── alerts.js       # Mock alert data
│   └── dashboard.js    # UI logic
└── README.md
```

## Use Case

This project demonstrates:
- Alert triage workflow understanding
- SOC dashboard design
- Prioritization logic (CVSS-based + contextual)
- Analyst documentation habits

## License

MIT
