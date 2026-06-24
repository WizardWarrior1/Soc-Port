# 📋 Incident Response Playbook

A comprehensive, markdown-based Incident Response (IR) playbook modeled after industry frameworks (NIST SP 800-61, SANS). Designed for SOC teams handling Tier 1–2 incidents. Includes playbooks for the most common attack scenarios.

## Included Playbooks

| # | Scenario | Severity |
|---|----------|----------|
| 1 | Ransomware Attack | P1 — Critical |
| 2 | Phishing / Business Email Compromise | P2 — High |
| 3 | Unauthorized Access / Account Compromise | P2 — High |
| 4 | Data Exfiltration | P1 — Critical |
| 5 | Malware / Endpoint Infection | P2 — High |
| 6 | DDoS Attack | P2 — High |
| 7 | Insider Threat | P1 — Critical |

## Framework

All playbooks follow the NIST IR lifecycle:

```
Preparation → Detection & Analysis → Containment → Eradication → Recovery → Post-Incident
```

## How to Use

1. Identify the incident type from initial triage
2. Open the relevant playbook in `playbooks/`
3. Follow each phase step-by-step, documenting actions in your ticketing system
4. Complete the **Post-Incident Report** template after closure

## Project Structure

```
incident-response-playbook/
├── README.md
├── playbooks/
│   ├── 01-ransomware.md
│   ├── 02-phishing-bec.md
│   ├── 03-account-compromise.md
│   ├── 04-data-exfiltration.md
│   ├── 05-malware-infection.md
│   ├── 06-ddos.md
│   └── 07-insider-threat.md
├── templates/
│   ├── incident-ticket-template.md
│   └── post-incident-report.md
└── references/
    └── escalation-matrix.md
```

## Severity Classification

| Priority | Response SLA | Description |
|----------|-------------|-------------|
| P1 — Critical | 15 min | Active breach, ransomware, data exfil |
| P2 — High | 1 hour | Compromised account, active malware |
| P3 — Medium | 4 hours | Suspicious activity, policy violation |
| P4 — Low | 24 hours | Informational, low-risk anomaly |

## References

- NIST SP 800-61r2: Computer Security Incident Handling Guide
- SANS Incident Handler's Handbook
- MITRE ATT&CK Framework

## License

MIT — Adapt freely for your organization's SOC.
