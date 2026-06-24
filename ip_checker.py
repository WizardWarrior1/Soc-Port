# 🕵️ Threat Intel Feed Aggregator

A Python tool that pulls from multiple open-source threat intelligence feeds, deduplicates and normalizes the data, and outputs a unified blocklist in multiple formats (plain text, CSV, Snort/Suricata rules).

## Features

- Pulls from AlienVault OTX, Abuse.ch URLhaus, Feodo Tracker, and CISA Known Exploited CVEs
- Normalizes IOC types: IPs, domains, URLs, file hashes
- Deduplicates across sources
- Outputs unified blocklist (IP, domain, hash)
- Generates Snort/Suricata rule snippets
- Schedulable via cron for daily updates

## Tech Stack

- Python 3.10+
- `requests`, `csv`, `json`, `hashlib`, `argparse`

## Setup

```bash
git clone https://github.com/yourusername/threat-intel-aggregator.git
cd threat-intel-aggregator
pip install -r requirements.txt
```

## Usage

```bash
# Pull all feeds and generate blocklist
python aggregator.py --all

# Pull specific feed only
python aggregator.py --feed urlhaus

# Output as Snort rules
python aggregator.py --all --format snort

# Schedule with cron (run daily at 6 AM)
0 6 * * * /usr/bin/python3 /opt/threat-intel/aggregator.py --all --output /etc/blocklist.txt
```

## Supported Feeds

| Feed | IOC Types | Update Frequency |
|------|-----------|-----------------|
| AlienVault OTX | IP, Domain, Hash, URL | Hourly |
| Abuse.ch URLhaus | URL, Domain | Live |
| Feodo Tracker | IP (C2 botnet) | Daily |
| CISA KEV | CVE IDs | As published |
| MalwareBazaar | File hashes | Daily |

## Sample Output

```
# Threat Intel Blocklist
# Generated: 2024-03-15 06:00:01 UTC
# Total IOCs: 14,832 IPs | 7,211 Domains | 3,944 Hashes

# ── IP BLOCKLIST ──
185.220.101.55   # Source: Feodo (Emotet C2) — Added: 2024-03-14
45.77.65.211     # Source: OTX (Brute force) — Added: 2024-03-13
...

# ── DOMAIN BLOCKLIST ──
malware-c2.ru    # Source: URLhaus — Added: 2024-03-15
...
```

## Project Structure

```
threat-intel-aggregator/
├── aggregator.py
├── feeds/
│   ├── otx.py
│   ├── urlhaus.py
│   ├── feodo.py
│   └── cisa_kev.py
├── output/
│   ├── blocklist.txt
│   └── blocklist.csv
├── requirements.txt
└── README.md
```

## License

MIT
