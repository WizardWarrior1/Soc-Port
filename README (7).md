# 📡 Network Traffic Analyzer

A Python-based packet capture analyzer that inspects PCAP files for suspicious network patterns. Detects port scans, beaconing behavior, DNS tunneling, and large data transfers using Scapy.

## Features

- Parses `.pcap` and `.pcapng` files
- Detects: port scans, beaconing (C2), DNS tunneling, data exfiltration
- Maps IPs to known threat intel blocklists
- Generates a color-coded terminal report
- Outputs findings as JSON

## Tech Stack

- Python 3.10+
- `scapy`, `collections`, `json`, `argparse`

## Setup

```bash
git clone https://github.com/yourusername/network-traffic-analyzer.git
cd network-traffic-analyzer
pip install -r requirements.txt
```

## Usage

```bash
# Analyze a PCAP file
python net_analyzer.py --file captures/sample.pcap

# Save findings to JSON
python net_analyzer.py --file captures/sample.pcap --output findings.json

# Enable verbose packet logging
python net_analyzer.py --file captures/sample.pcap --verbose
```

## Detection Capabilities

| Detection | Method | Threshold |
|-----------|--------|-----------|
| Port Scan | Unique destination ports per source IP | >15 ports/60s |
| C2 Beacon | Periodic connection intervals to single IP | Stddev < 2s |
| DNS Tunneling | Abnormally long DNS query names | >50 chars |
| Data Exfil | Large outbound transfers to external IPs | >100 MB |
| Non-standard Ports | Common services on non-default ports | e.g., HTTP on 8888 |

## Sample Output

```
[SCAN DETECTED]     192.168.1.105 → 10.0.0.1 scanned 47 ports in 58 seconds
[C2 BEACON]         10.0.2.33 → 185.220.101.55 — interval: 30.01s ±0.4s (12 connections)
[DNS TUNNEL]        Suspiciously long query: exfiltrateddata.encoded.c2domain.ru (67 chars)
[DATA EXFIL]        10.0.1.22 → 203.0.113.50: 247 MB transferred over 4 minutes
```

## Project Structure

```
network-traffic-analyzer/
├── net_analyzer.py
├── detectors/
│   ├── port_scan.py
│   ├── beaconing.py
│   └── dns_tunnel.py
├── captures/
│   └── sample.pcap     # Sample capture for testing
├── requirements.txt
└── README.md
```

## License

MIT
