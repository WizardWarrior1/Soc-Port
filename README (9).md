# 🎣 Phishing Email Detector

A Python tool that analyzes raw email files (.eml) for phishing indicators of compromise (IOCs). Inspects headers, links, attachments, and sender reputation to produce a threat score and detailed breakdown.

## Features

- Parses `.eml` files and extracts full header chains
- Checks SPF, DKIM, and DMARC alignment
- Extracts and scans all URLs using regex + optional VirusTotal API
- Flags suspicious sender patterns and domain spoofing
- Scores each email 0–100 (Higher = more suspicious)
- Outputs a color-coded terminal report

## Tech Stack

- Python 3.10+
- `email`, `re`, `dns.resolver`, `requests`

## Setup

```bash
git clone https://github.com/yourusername/phishing-email-detector.git
cd phishing-email-detector
pip install -r requirements.txt

# Optional: add VirusTotal API key to .env
echo "VT_API_KEY=your_key_here" > .env
```

## Usage

```bash
# Analyze a single .eml file
python phishing_detector.py --file samples/suspicious.eml

# Analyze with VirusTotal URL scanning
python phishing_detector.py --file samples/suspicious.eml --vt-scan

# Output JSON report
python phishing_detector.py --file samples/suspicious.eml --output report.json
```

## Scoring Breakdown

| Check | Max Points |
|-------|-----------|
| SPF fail | +25 |
| DKIM fail | +20 |
| DMARC fail | +15 |
| Mismatched From/Reply-To | +15 |
| Suspicious URLs detected | +10 per URL (max 30) |
| Punycode/homoglyph domain | +20 |
| Credential-harvesting keywords | +10 |

**Score Interpretation:**
- `0–20`: Clean ✅
- `21–50`: Suspicious ⚠️
- `51–100`: Likely Phishing 🚨

## Sample Output

```
═══════════════════════════════════════
  PHISHING ANALYSIS REPORT
═══════════════════════════════════════
File:       suspicious.eml
From:       "PayPal Security" <security@paypa1.com>
Subject:    URGENT: Verify your account
Date:       Mon, 15 Mar 2024 03:12:00 -0500

[FAIL] SPF:   No SPF record for paypa1.com
[FAIL] DKIM:  Signature not present
[WARN] URL:   http://paypa1.com/login  → Redirect to 91.234.55.12
[WARN] Homoglyph domain detected: paypa1.com (l → 1)

Threat Score: 85/100  🚨 LIKELY PHISHING
```

## Project Structure

```
phishing-email-detector/
├── phishing_detector.py
├── modules/
│   ├── header_analyzer.py
│   ├── url_extractor.py
│   ├── dns_checker.py
│   └── scoring.py
├── samples/
│   └── suspicious.eml
├── requirements.txt
└── .env.example
```

## License

MIT
