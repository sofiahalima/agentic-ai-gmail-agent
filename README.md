# Gmail Autonomous Agent — LangGraph + LLM Decision Pipeline

An agentic workflow that automatically reviews Gmail messages, applies LLM reasoning, and safely deletes unwanted emails with built-in guardrails, logging, and Slack monitoring.

This project demonstrates how to build a real autonomous agent pipeline — not just an LLM script — using structured decision flow, safety layers, and scheduled execution.

---

## 🚀 Features

- Autonomous Gmail review pipeline
- LLM-based decision reasoning
- Safety guardrails to prevent unsafe deletes
- LangGraph workflow orchestration
- Slack reporting after every run
- Structured logging + audit trail
- Cron-ready scheduling
- Confidence-aware decision protection

---

## 🧠 Agent Architecture

The system runs as a deterministic agent graph:

```
fetch → decide → delete → log → summary → alert
```

### Nodes

**Fetch**
- Pulls Gmail messages using Gmail API

**Decide**
- LLM evaluates email intent
- Outputs structured decision:
  - DELETE
  - KEEP
  - UNSURE

**Delete**
- Applies safety thresholds
- Low-confidence deletes are protected

**Log**
- Writes structured audit entries

**Summary**
- Generates run statistics

**Alert**
- Sends Slack notification

---

## 🔒 Safety Design

The agent does **not blindly delete emails**.

Protection includes:

- Confidence threshold gating
- LLM decision auditing
- Low-confidence safeguards
- Explicit delete filtering

This mirrors real-world agent safety patterns.

---

## 🛠 Tech Stack

- Python 3.11+
- LangGraph (agent orchestration)
- Gmail API
- Slack Webhooks
- Requests
- Structured logging

---

## 📦 Installation

### Clone repo

```bash
git clone <repo-url>
cd gmail-agent
```

### Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create `.env`:

```
SLACK_WEBHOOK_URL=your_webhook_here
```

Google OAuth credentials:

```
credentials.json
```

Run once to generate Gmail token:

```bash
python run_graph.py
```

---

## ▶ Run Agent

Manual run:

```bash
python run_graph.py
```

Scheduled run (example weekly cron):

```
0 9 * * 0 /path/to/.venv/bin/python run_graph.py
```

---

## 📊 Example Slack Summary

```
Gmail Agent Weekly Report

Processed: 20
Proposed deletes: 2
Deleted: 1
Protected: 1
Keep: 16
Unsure: 1
```

---

## 🧪 Logging

All decisions are logged for auditing:

```
logs/gmail_agent.log
```

---

## 🔮 Future Extensions

- Human-in-the-loop approval mode
- Confidence drift monitoring
- Dashboard reporting
- Multi-account orchestration
- Batch parallel processing

---

## 🎯 Purpose

This project demonstrates:

- Agent orchestration patterns
- LLM decision safety pipelines
- autonomous workflow design
- production-style monitoring

It is meant as a template for real-world agent systems.

---

## ⚠ Disclaimer

Always test on non-critical email accounts.  
LLMs are probabilistic systems — guardrails are essential.

---


