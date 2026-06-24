# 🔎 Vulnerability Scanner Report Parser

A Python utility that parses Nessus (`.nessus` XML) and OpenVAS (`.xml`) vulnerability scan reports and converts them into clean, prioritized CSV or HTML reports. Built for SOC and Vulnerability Management analysts.

## Features

- Parses `.nessus` (Nessus v2 XML) and OpenVAS XML formats
- Extracts: host, port, plugin ID, vulnerability name, severity, CVE, CVSS score, description, solution
- Sorts findings by CVSS score descending
- Filters by minimum severity (Critical, High, Medium, Low, Info)
- Generates clean HTML report or CSV export
- Shows remediation summary by host

## Tech Stack

- Python 3.10+
- `xml.etree.ElementTree`, `csv`, `html`, `argparse`

## Setup

```bash
git clone https://github.com/yourusername/vuln-scanner-parser.git
cd vuln-scanner-parser
pip install -r requirements.txt
```

## Usage

```bash
# Parse Nessus file, show Critical and High only
python vuln_parser.py --file scan.nessus --min-severity high

# Export to CSV
python vuln_parser.py --file scan.nessus --output report.csv --format csv

# Export to HTML report
python vuln_parser.py --file scan.nessus --output report.html --format html

# Parse OpenVAS XML
python vuln_parser.py --file openvas_scan.xml --scanner openvas --format html
```

## Sample Output (Terminal)

```
╔══════════════════════════════════════════════════════════════════╗
║  VULNERABILITY REPORT — scan.nessus
║  Hosts: 12 | Total Findings: 247 | Critical: 8 | High: 41
╠══════════════════════════════════════════════════════════════════╣
║ CVSS  │ Host            │ Port  │ Vulnerability
╠══════════════════════════════════════════════════════════════════╣
║ 10.0  │ 10.0.1.55       │ 445   │ MS17-010: EternalBlue
║  9.8  │ 10.0.1.22       │ 3389  │ CVE-2019-0708 BlueKeep
║  9.1  │ 10.0.2.100      │ 443   │ Apache Log4Shell (CVE-2021-44228)
║  8.8  │ 10.0.1.44       │ 80    │ Apache Struts RCE (CVE-2017-5638)
╚══════════════════════════════════════════════════════════════════╝
```

## Project Structure

```
vuln-scanner-parser/
├── vuln_parser.py
├── parsers/
│   ├── nessus_parser.py
│   └── openvas_parser.py
├── templates/
│   └── report.html.jinja
├── samples/
│   └── sample_scan.nessus
└── README.md
```

## License

MIT
