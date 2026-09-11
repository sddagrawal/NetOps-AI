# Intelligent Network Operations System (NetOps-AI)

An autonomous, closed-loop network operation and incident management platform designed for enterprise network reliability and safety verification.

The platform implements a complete 6-stage lifecycle for network telemetry analysis and automated remediation:

$$\text{Detect} \longrightarrow \text{Understand} \longrightarrow \text{Plan} \longrightarrow \text{Evaluate} \longrightarrow \text{Simulate} \longrightarrow \text{Safely Respond}$$

---

## Key Features

- **Graph-Based Topology Engine**: Uses NetworkX directed graphs to model physical network devices, traffic direction, capacity limits, and dependency chains.
- **Explainable Anomaly Detection**: Evaluates telemetry streams (CPU, latency, packet loss, bandwidth) against operational baselines without opaque ML "black boxes."
- **Root Cause Analysis (RCA)**: Distinguishes between downstream symptoms and original failure points using graph traversal algorithms.
- **Operational vs. Security Classification**: Differentiates standard infrastructure failures from potential security threats (e.g., data exfiltration vs. scheduled backups).
- **Digital Twin What-If Simulator**: Clones the active network state and simulates the effect of proposed fixes before executing them in production.
- **Safety Policy & Decision Engine**: Evaluates safety constraints to decide whether an action should be **AUTO-EXECUTED**, require **HUMAN APPROVAL**, or be **REJECTED**.

---

## Directory Structure

```text
netops-ai/
│
├── backend/
│   ├── app.py                      # Flask API Server & Lifecycle Controller
│   ├── network_model.py            # Graph Topology & Dependency Engine (NetworkX)
│   ├── telemetry.py                # Telemetry Stream Generator
│   ├── anomaly_detector.py         # Rule-Based Anomaly Detection Logic
│   ├── root_cause.py               # Dependency-Aware Root Cause Engine
│   ├── security_classifier.py      # Event Security & Intent Classifier
│   ├── action_planner.py           # Remediation Strategy Generator
│   ├── safety_engine.py            # Safety Rules & Policy Validator
│   ├── simulator.py                # Digital Twin What-If Simulation Engine
│   └── decision_engine.py          # Decision Synthesis Engine
│
├── frontend/
│   ├── index.html                  # Dashboard Layout
│   ├── style.css                   # Enterprise Cisco Dark Theme
│   └── script.js                   # Topology Rendering & API Communication
│
├── data/
│   └── scenarios.json              # Incident Simulation Scenarios
│
├── requirements.txt                # Python Dependencies
└── README.md                       # Project Documentation & Guide