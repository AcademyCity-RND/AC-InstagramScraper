# Security Policy for AC-InstagramScraper

## 1. Disclaimer

By using **AC-InstagramScraper**, you agree to comply with all applicable local and international laws, terms of service, copyright, and privacy regulations. The developers and contributors of AC-InstagramScraper will not be held liable for any misuse, abuse, or unauthorized data extraction activities conducted using this software. It is the user's sole responsibility to ensure ethical, responsible, and compliant usage in educational, research, and authorized forensic auditing contexts.

## 2. Supported Versions

We provide active security updates and dependency maintenance for the following branches:

| Branch | Supported | Notes |
| :--- | :--- | :--- |
| `master` | :white_check_mark: | Active production release & CI/CD verified |
| `feat/*` | :warning: | Feature branches (under active testing) |

## 3. Reporting a Vulnerability

We take the security and stability of the AC-InstagramScraper engine very seriously:

1. If you discover a security vulnerability or sensitive bug, please **do not open a public issue**.
2. Instead, report it responsibly via **GitHub Private Vulnerability Reporting** through the Security tab of the repository:
   - [https://github.com/AcademyCity-RND/AC-InstagramScraper/security/advisories](https://github.com/AcademyCity-RND/AC-InstagramScraper/security/advisories)
3. Please include detailed steps to reproduce the issue, proof of concept (PoC), and potential mitigation.
4. We aim to acknowledge and address all valid security disclosures promptly.

## 4. Automated Security Audits

This repository enforces automated vulnerability audits on every push, pull request, and weekly schedule using `pip-audit` via GitHub Actions to ensure zero known vulnerabilities in our dependency tree.
