Markdown
# LLM Package Hallucination Suite & Slop-Guard 🛡️

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security: Environment-Variables](https://img.shields.io/badge/Security-API%20Keys%20Protected-brightgreen.svg)]()
[![Registry Check: PyPI](https://img.shields.io/badge/PyPI-Real--time%20Verification-informational.svg)](https://pypi.org/)

An empirical security benchmark suite and real-time command-line firewall designed to detect, analyze, and prevent risks associated with **LLM package hallucinations** and **slopsquatting**.

---

## 📌 Overview

Large Language Models (LLMs) frequently hallucinate non-existent package names when writing code snippets (e.g., recommending `pip install missing-package-name`). Malicious actors can register these hallucinated package names on public registries (PyPI) to execute automated code injection—a technique known as **slopsquatting**.

**LLM Package Hallucination Suite** delivers a dual-layer defense system:
1. **Real-time CLI Firewall (`slop_guard.py`)**: Intercepts `pip install` commands before execution, verifies package existence against PyPI's live API, and blocks attempts to install non-existent or dangerous packages.
2. **Empirical Benchmark Scanner (`batch_detector.py`)**: Evaluates multi-model LLM responses across domain-specific code prompts to quantify package hallucination rates.

---

## ✨ Key Features

- 🛑 **Real-Time PyPI Verification**: Queries official PyPI JSON endpoints (`https://pypi.org/pypi/<package>/json`) before allow-listing installation commands.
- 🧪 **Multi-Model Benchmark Analysis**: Evaluates leading models (e.g., Llama, Mixtral) via Groq API to measure hallucination frequency across Python domains.
- 📊 **Automated Visual Analytics**: Generates clear statistical charts (`chart_model_vulnerability.png`, `chart_domain_breakdown.png`) using `matplotlib` and `seaborn`.
- 🔐 **Zero Secret Leakage**: Fully decouples API keys from source code by enforcing system environment variable loading (`os.environ.get("GROQ_API_KEY")`).

---

## 📁 Repository Structure

```text
llm-package-hallucination-suite/
├── .gitignore                      # Prevents sensitive files (.env, keys) from committing
├── README.md                       # Repository documentation
├── slop_guard.py                   # Real-time CLI firewall and pip guard utility
├── batch_detector.py               # Benchmark scanner executing multi-model LLM prompts
├── hallucination_detector.py       # Core package extraction and validation logic
├── plot_results.py                 # Analytics generator producing research charts
├── multi_model_hallucinations.csv  # Raw benchmark dataset across tested LLMs
└── hallucinations_dataset.csv      # Processed evaluation dataset

⚡ Quick Start & Installation
1. Prerequisites

Python 3.9 or higher
Git

2. Clone the Repository

git clone [https://github.com/malkamanuranga/llm-package-hallucination-suite.git](https://github.com/malkamanuranga/llm-package-hallucination-suite.git)

cd llm-package-hallucination-suite

3. Install Dependencies

pip install requests pandas matplotlib seaborn

⚙️ Environment Configuration

This project requires a Groq API key for executing the benchmark scanner. Never hardcode your API key into source files.

Setting Environment Variables

1.On Windows (Command Prompt):

set GROQ_API_KEY=gsk_your_actual_api_key_here

2.On Windows (PowerShell):

$env:GROQ_API_KEY="gsk_your_actual_api_key_here"

3.On Linux / macOS:

export GROQ_API_KEY="gsk_your_actual_api_key_here"

🚀 Usage Guide
1. Run the Real-Time CLI Guard (slop_guard.py)
Safely validate any package before running pip install:


python slop_guard.py --check <package_name>
If the package is not found on PyPI, slop-guard raises a security alert and halts execution.

2. Run the Multi-Model Benchmark Scanner (batch_detector.py)
Run empirical evaluation across domain prompts and LLM models:


python batch_detector.py
Outputs structured CSV results to multi_model_hallucinations.csv.

3. Generate Analytical Visualizations (plot_results.py)
Transform evaluation datasets into high-resolution research charts:


python plot_results.py
Generates:

chart_model_vulnerability.png: Hallucination rate comparison by LLM model.

chart_domain_breakdown.png: Package vulnerability distribution across technical domains.

🔒 Security & Safe Disclosure
API Safety: No secret keys, passwords, or personal credentials are stored in this repository.

Local Isolation: All .env, keys.txt, and virtual environments (.venv) are strictly excluded via .gitignore.

Registry Privacy: All verification calls are read-only HTTP GET requests sent directly to https://pypi.org/.

📄 License
Distributed under the MIT License. See LICENSE for details.


