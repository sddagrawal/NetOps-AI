from flask import Flask, jsonify, request, send_from_directory
import os

from network_model import NetworkGraph
from telemetry import TelemetryEngine
from anomaly_detector import AnomalyDetector
from root_cause import RootCauseAnalyzer
from security_classifier import SecurityClassifier
from action_planner import ActionPlanner
from simulator import WhatIfSimulator
from safety_engine import SafetyEngine
from decision_engine import DecisionEngine

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Initialize System Modules
net_model = NetworkGraph()
telemetry_engine = TelemetryEngine(net_model)
anomaly_detector = AnomalyDetector()
root_cause_analyzer = RootCauseAnalyzer(net_model)
security_classifier = SecurityClassifier()
action_planner = ActionPlanner()
simulator = WhatIfSimulator()
safety_engine = SafetyEngine()
decision_engine = DecisionEngine()

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/api/topology", methods=["GET"])
def get_topology():
    return jsonify(net_model.get_topology_dict())

@app.route("/api/process_scenario", methods=["POST"])
def process_scenario():
    data = request.json or {}
    scenario = data.get("scenario", "NORMAL")

    # Pipeline Execution
    telemetry = telemetry_engine.get_telemetry(scenario)
    anomalies = anomaly_detector.analyze(telemetry)
    rca = root_cause_analyzer.identify_root_cause(scenario, anomalies, telemetry)
    sec_class = security_classifier.classify(scenario, rca)
    plan = action_planner.generate_plans(scenario)
    sim_result = simulator.simulate_action(telemetry, plan)
    safety_eval = safety_engine.evaluate(plan, sim_result, net_model)
    final_decision = decision_engine.make_decision(safety_eval)

    return jsonify({
        "scenario": scenario,
        "telemetry": telemetry,
        "anomalies": anomalies,
        "root_cause": rca,
        "security_classification": sec_class,
        "action_plan": plan,
        "simulation": sim_result,
        "safety_evaluation": safety_eval,
        "final_decision": final_decision
    })

if __name__ == "__main__":
    print("🚀 Starting Cisco NetOps-AI Backend Engine on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)