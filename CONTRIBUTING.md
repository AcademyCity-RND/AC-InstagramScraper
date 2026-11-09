# Contributing to AC-InstagramScraper

Thank you for your interest in contributing to **AC-InstagramScraper**! We welcome contributions, bug reports, feature requests, and documentation improvements from developers, researchers, and open-source enthusiasts.

Please take a few moments to review these guidelines before submitting a contribution.

---

## 🧭 Code of Conduct & Ethical Scraping

1. **Responsible & Ethical Research**: This project is developed strictly for educational, research, and authorized digital forensics auditing. Automated scraping must always be conducted responsibly, respecting platform rate limits, human pacing delays, and privacy regulations.
2. **Respectful Collaboration**: Maintain a welcoming, inclusive, and professional environment for all contributors. Harassment or derogatory behavior of any kind will not be tolerated.

---

## 🛠️ Local Development Setup

### 1. Prerequisites
- **Python 3.11** (recommended and verified across our CI/CD pipeline)
- **Git**
- **Docker** (optional, for containerized testing)

### 2. Fork and Clone
```bash
# 1. Fork the repository on GitHub:
# https://github.com/AcademyCity-RND/AC-InstagramScraper

# 2. Clone your personal fork:
git clone https://github.com/<your-username>/AC-InstagramScraper.git
cd AC-InstagramScraper

# 3. Add the upstream repository:
git remote add upstream https://github.com/AcademyCity-RND/AC-InstagramScraper.git
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Linux / macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Upgrade pip and install all dependencies (core + development tools)
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## 🌿 Branching Strategy

To keep git history clean, readable, and atomic:

1. Always branch off the latest `master`:
   ```bash
   git checkout master
   git pull upstream master
   git checkout -b <branch-type>/<short-description>
   ```
2. Branch naming conventions:
   - `feat/<feature-name>`: New features, endpoints, or data parsers.
   - `fix/<bug-name>`: Bug fixes and upstream schema adjustment patches.
   - `docs/<topic>`: Documentation updates, diagrams, or guide improvements.
   - `ci/<workflow>`: CI/CD workflows, Dependabot, or build script tweaks.
   - `test/<test-name>`: Test suite expansion and validation fixtures.

---

## 📝 Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) standards. Please write clear, concise commit messages using one of the following prefixes:

- `feat:` A new feature or endpoint
- `fix:` A bug fix or patch
- `docs:` Documentation only changes
- `style:` Formatting, missing semicolons, whitespace (no functional changes)
- `refactor:` Code refactoring that neither fixes a bug nor adds a feature
- `test:` Adding missing tests or correcting existing tests
- `build:` Changes that affect the build system or external dependencies
- `ci:` Changes to our CI configuration files and automation scripts

**Example:**
```bash
git commit -m "feat(adapter): add support for Instagram Threads cross-post reference"
```

---

## 🧪 Testing & Code Quality Gates

All contributions must pass local quality checks before opening a Pull Request:

### 1. Run the Test Suite
```bash
pytest -v
```

### 2. Run Linting & Syntax Verification
```bash
# Verify no syntax errors or undefined symbols
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=.git,__pycache__,output

# Check general PEP8 adherence
flake8 . --count --max-complexity=15 --max-line-length=127 --statistics --exclude=.git,__pycache__,output
```

### 3. Run Security Vulnerability Audit
```bash
pip-audit -r requirements.txt
```

---

## 🔀 Pull Request Guidelines

1. **Keep PRs Focused**: Each Pull Request should address one clear bug, feature, or improvement. Avoid mixing unrelated changes.
2. **Update Tests & Documentation**: If you add a new endpoint or modify a parser, include corresponding unit tests in `tests/` and document it in `README.md`.
3. **Verify CI Status**: Ensure all GitHub Actions checks (CI Pipeline and Security Audit) pass with green checks.
4. **Never Commit Secrets**: Never commit personal `.env` files, API keys, credentials, or private session cookies.

---

## 💬 Questions & Feedback

For questions, discussions, or proposals:
- Open an issue on GitHub: [https://github.com/AcademyCity-RND/AC-InstagramScraper/issues](https://github.com/AcademyCity-RND/AC-InstagramScraper/issues)
- For security vulnerabilities, review [SECURITY.md](SECURITY.md) and report via GitHub Private Vulnerability Reporting.
