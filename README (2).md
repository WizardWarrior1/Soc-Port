# Playbook 01: Ransomware Attack

**Severity:** P1 — Critical  
**SLA:** Respond within 15 minutes of detection  
**Last Updated:** 2024-03-01  
**Owner:** SOC Team Lead

---

## Detection Triggers

- EDR alert: Mass file encryption activity
- SIEM alert: Ransomware file extensions created (`.locked`, `.encrypted`, `.WNCRY`)
- User reports: Files inaccessible, ransom note on screen
- Shadow copy deletion detected (`vssadmin delete shadows`)

---

## Phase 1: Identification (0–15 min)

- [ ] Assign incident ticket (Priority: P1)
- [ ] Identify affected endpoint(s) via EDR console
- [ ] Determine patient zero (first infected host)
- [ ] Identify the ransomware family (use ID-Ransomware.com)
- [ ] Check for lateral movement to other hosts
- [ ] Notify SOC Lead and Incident Commander immediately
- [ ] Do NOT reboot or shutdown affected systems yet

**Key Questions:**
- How many hosts are affected?
- Is the encryption still ongoing?
- Has any data been exfiltrated (double extortion)?
- Are backups intact and isolated?

---

## Phase 2: Containment (15–60 min)

- [ ] **Network Isolation:** Quarantine infected hosts at the switch/firewall level
- [ ] **Disable accounts:** Disable any service accounts active on infected hosts
- [ ] **Block C2:** Identify and block attacker C2 domains/IPs at the firewall
- [ ] **Preserve evidence:** Take memory dump before any remediation
  ```bash
  winpmem_mini_x64_rc2.exe memdump.raw
  ```
- [ ] **Do not pay ransom** without executive and legal sign-off
- [ ] Notify: CISO, Legal, PR (if customer data involved)
- [ ] Check whether backups are encrypted or affected

---

## Phase 3: Eradication

- [ ] Identify and remove the ransomware binary from all hosts
- [ ] Check and remove persistence mechanisms:
  - Registry Run keys
  - Scheduled tasks
  - WMI subscriptions
- [ ] Reset all credentials for affected users and service accounts
- [ ] Patch the initial access vector (e.g., vulnerable VPN, RDP, phishing link)
- [ ] Perform full AV/EDR scan on all hosts in the environment

---

## Phase 4: Recovery

- [ ] Restore systems from clean, pre-infection backups
- [ ] Validate backup integrity before restoration
- [ ] Bring systems back online in isolation first for testing
- [ ] Monitor restored systems closely for 72 hours
- [ ] Notify affected users once systems are confirmed clean

---

## Phase 5: Post-Incident

- [ ] Complete Post-Incident Report (see `templates/post-incident-report.md`)
- [ ] Submit ransomware sample to:
  - VirusTotal
  - FBI IC3 (www.ic3.gov)
  - CISA (report@cisa.dhs.gov)
- [ ] Update threat intel blocklists with observed IOCs
- [ ] Schedule lessons-learned meeting within 5 business days
- [ ] Update playbook with new findings

---

## Evidence Checklist

| Evidence Type | Location | Collected? |
|--------------|----------|------------|
| Memory dump | `/forensics/memdump.raw` | ☐ |
| Disk image | `/forensics/disk.img` | ☐ |
| Windows Event Logs | `/forensics/evtx/` | ☐ |
| EDR telemetry export | SIEM/EDR console | ☐ |
| Network PCAP | `/forensics/capture.pcap` | ☐ |
| Ransom note | `/forensics/ransom_note.txt` | ☐ |

---

## Escalation Path

```
SOC Analyst → SOC Lead → Incident Commander → CISO → Legal/PR
```

---

## Common Ransomware Families & Resources

| Family | Decryptor Available | Reference |
|--------|-------------------|-----------|
| WannaCry | Yes | No More Ransom |
| REvil / Sodinokibi | Partial | No More Ransom |
| LockBit | No | N/A |
| BlackCat (ALPHV) | No | FBI Advisory |
| Ryuk | No | CISA Alert |
