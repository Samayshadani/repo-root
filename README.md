# 🔐 AI-Powered GitHub Action – Skills Security Scanner

## 📌 Overview

This project implements an AI-powered GitHub Action that scans markdown files inside a `skills/` folder and detects malicious or unsafe instructions automatically.

The goal is to build a security guardrail that prevents unsafe AI skill files (such as prompt injections or data exfiltration attempts) from being merged into the main branch.

The workflow runs on:

- Push to `main`
- Pull Requests

If HIGH severity malicious content is detected, the workflow fails automatically.

---

## 🧠 Problem Statement

In modern AI tooling, skills are structured markdown files that define reusable AI behaviors or instructions.

Because these files may influence agent execution logic, they can become security risks if they contain:

- Prompt injection
- Hidden system override commands
- Data exfiltration attempts
- Jailbreak instructions

This project builds an automated CI-based guardrail system to detect such threats before code is merged.

---

## 🏗️ Architecture

Repository Structure:

repo-root/
│
├── .github/workflows/scan-skills.yml
├── skills/
│ ├── safe_skill.md
│ ├── suspicious_skill.md
│ └── malicious_skill.md
│
├── scanner/
│ ├── scan.py
│ ├── cache.json
│ └── ignore_list.txt
│
├── requirements.txt
└── README.md

---

## ⚙️ How It Works

1. GitHub Action triggers on push or pull request.
2. The workflow installs Python and Ollama.
3. The scanner reads all `.md` files inside `skills/`.
4. Each file is sent to a local LLM (via Ollama).
5. The model classifies content into:
   - SAFE
   - LOW
   - HIGH
6. If HIGH severity is detected:
   - The workflow exits with a non-zero code
   - CI fails
   - The PR is blocked

---

## 🤖 AI Model Used

This project uses **Ollama** with the `llama3` model.

Why Ollama?

- No API key required
- No quota limitations
- Fully local and reproducible
- Free to use
- No external billing dependency

This ensures the CI pipeline is self-contained and cost-efficient.

---

## 🚦 Severity Levels

The AI classifies each file into:

### ✅ SAFE
No malicious or suspicious content detected.

### ⚠️ LOW
Suspicious behavior detected (e.g., instruction override patterns), but not clearly malicious.

The workflow continues.

### ❌ HIGH
Clear malicious intent detected (e.g., data exfiltration, secret leakage, system override).

The workflow fails automatically.

---

## 🔄 Caching

The scanner implements file-hash caching.

- Each file’s SHA256 hash is stored in `cache.json`
- Unchanged files are skipped during scanning
- Improves performance and reduces unnecessary AI calls

Note: GitHub runners are ephemeral environments. Cache persistence across runs would require GitHub caching mechanisms in production.

---

## 📝 Ignore List

An `ignore_list.txt` file allows safe phrases to be excluded from triggering warnings.

This prevents documentation examples from being flagged as malicious.

---

## 🚀 Running Locally

### 1️⃣ Install Ollama

Download from:
https://ollama.com/download

Pull model:

---

### 2️⃣ Install Python dependencies

---

### 3️⃣ Run Scanner

---

## 🔄 GitHub Action Workflow

The workflow is located at:

It runs automatically on:

- Push to main
- Pull requests

If HIGH severity is detected, the workflow fails.

---

## 🎯 Demo Flow

1. Add malicious instruction inside a skill file.
2. Push to repository.
3. GitHub Action runs.
4. Workflow fails due to HIGH severity.
5. Remove malicious content.
6. Push again.
7. Workflow passes.

---

## 🛡️ Security Design Thinking

This project demonstrates:

- AI-based semantic threat detection (instead of simple regex)
- CI/CD guardrail design
- Severity-based triaging
- Automated security enforcement
- DevSecOps thinking
- Reproducible infrastructure

---

## 📹 Demo Video

The demo video explains:

- What skills are
- Security risks
- Architecture design
- Why Ollama was chosen
- Live CI failure example
- Successful remediation

---

## ✅ Evaluation Highlights

✔ Clean repository structure  
✔ Automated CI integration  
✔ AI-based classification  
✔ Security-first design  
✔ Observability via logs  
✔ Production-aware decisions  

---

## 👨‍💻 Author

Samay
