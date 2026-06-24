#!/usr/bin/env python3
"""
Vulnerability Scanner Report Parser
Parses Nessus .nessus XML files and outputs clean, prioritized reports.
"""

import xml.etree.ElementTree as ET
import csv
import html
import argparse
import os
from dataclasses import dataclass, field
from typing import Optional

SEVERITY_MAP = {0: "Info", 1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
MIN_SEVERITY_FILTER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

SEVERITY_COLORS = {
    "Critical": "#d73a49",
    "High":     "#e36209",
    "Medium":   "#b08800",
    "Low":      "#2188ff",
    "Info":     "#6a737d",
}


@dataclass
class Vulnerability:
    host: str
    port: str
    protocol: str
    plugin_id: str
    name: str
    severity: str
    severity_num: int
    cvss_score: float
    cve: list[str] = field(default_factory=list)
    description: str = ""
    solution: str = ""
    plugin_output: str = ""


def parse_nessus(filepath: str, min_severity: int = 0) -> list[Vulnerability]:
    """Parse a .nessus XML file and return a list of Vulnerability objects."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    findings = []

    for host in root.findall(".//ReportHost"):
        hostname = host.get("name", "unknown")

        for item in host.findall("ReportItem"):
            sev_num = int(item.get("severity", 0))
            if sev_num < min_severity:
                continue

            cves = [c.text for c in item.findall("cve") if c.text]
            cvss_raw = item.findtext("cvss_base_score", "0.0")
            try:
                cvss = float(cvss_raw)
            except ValueError:
                cvss = 0.0

            findings.append(Vulnerability(
                host=hostname,
                port=item.get("port", "0"),
                protocol=item.get("protocol", "tcp"),
                plugin_id=item.get("pluginID", ""),
                name=item.get("pluginName", "Unknown"),
                severity=SEVERITY_MAP.get(sev_num, "Unknown"),
                severity_num=sev_num,
                cvss_score=cvss,
                cve=cves,
                description=(item.findtext("description") or "").strip()[:300],
                solution=(item.findtext("solution") or "").strip()[:200],
                plugin_output=(item.findtext("plugin_output") or "").strip()[:200],
            ))

    # Sort by CVSS descending, then severity descending
    findings.sort(key=lambda v: (v.cvss_score, v.severity_num), reverse=True)
    return findings


def print_terminal_report(findings: list[Vulnerability]):
    counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1

    hosts = len(set(f.host for f in findings))
    print("\n" + "═" * 70)
    print(f"  VULNERABILITY REPORT")
    print(f"  Hosts: {hosts} | Total: {len(findings)} | "
          + " | ".join(f"{s}: {n}" for s, n in sorted(counts.items(), key=lambda x: -SEVERITY_MAP.get(x[0], 0) if isinstance(SEVERITY_MAP.get(x[0], 0), int) else 0)))
    print("═" * 70)
    print(f"{'CVSS':>6}  {'Sev':<10} {'Host':<18} {'Port':<7} {'Vulnerability'}")
    print("─" * 70)
    for f in findings[:50]:  # Show top 50
        cve_str = f.cve[0] if f.cve else ""
        print(f"{f.cvss_score:>6.1f}  {f.severity:<10} {f.host:<18} {f.port:<7} {f.name[:35]}")
        if cve_str:
            print(f"{'':>6}  {'':10} {cve_str}")
    print("═" * 70 + "\n")


def export_csv(findings: list[Vulnerability], filepath: str):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Host", "Port", "Protocol", "Severity", "CVSS", "Plugin ID", "Vulnerability", "CVEs", "Solution"])
        for v in findings:
            writer.writerow([
                v.host, v.port, v.protocol, v.severity, v.cvss_score,
                v.plugin_id, v.name, "; ".join(v.cve), v.solution,
            ])
    print(f"[+] CSV saved: {filepath}")


def export_html(findings: list[Vulnerability], filepath: str):
    rows = ""
    for v in findings:
        color = SEVERITY_COLORS.get(v.severity, "#6a737d")
        cves = ", ".join(v.cve) if v.cve else "—"
        rows += f"""
        <tr>
          <td>{html.escape(v.host)}</td>
          <td>{v.port}</td>
          <td><span style="color:{color};font-weight:bold">{v.severity}</span></td>
          <td>{v.cvss_score}</td>
          <td>{html.escape(v.name)}</td>
          <td>{html.escape(cves)}</td>
          <td style="font-size:0.8em">{html.escape(v.solution[:120])}</td>
        </tr>"""

    template = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Vuln Report</title>
<style>
body{{font-family:Arial,sans-serif;background:#0d1117;color:#e6edf3;padding:20px}}
h1{{color:#58a6ff}}table{{width:100%;border-collapse:collapse;font-size:0.85rem}}
th{{background:#21262d;padding:8px;text-align:left;color:#8b949e}}
td{{padding:8px;border-bottom:1px solid #21262d}}
</style></head><body>
<h1>Vulnerability Report</h1>
<p>Total findings: {len(findings)}</p>
<table><thead><tr>
<th>Host</th><th>Port</th><th>Severity</th><th>CVSS</th>
<th>Vulnerability</th><th>CVEs</th><th>Solution</th>
</tr></thead><tbody>{rows}</tbody></table>
</body></html>"""

    with open(filepath, "w") as f:
        f.write(template)
    print(f"[+] HTML report saved: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Vulnerability Scanner Report Parser")
    parser.add_argument("--file", required=True, help="Path to .nessus or OpenVAS XML file")
    parser.add_argument("--min-severity", default="info", choices=MIN_SEVERITY_FILTER.keys())
    parser.add_argument("--format", default="terminal", choices=["terminal", "csv", "html"])
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}")
        return

    min_sev = MIN_SEVERITY_FILTER[args.min_severity]
    findings = parse_nessus(args.file, min_severity=min_sev)
    print(f"[*] Parsed {len(findings)} findings from {args.file}")

    if args.format == "terminal":
        print_terminal_report(findings)
    elif args.format == "csv":
        export_csv(findings, args.output or "report.csv")
    elif args.format == "html":
        export_html(findings, args.output or "report.html")


if __name__ == "__main__":
    main()
