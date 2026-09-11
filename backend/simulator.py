import copy

class WhatIfSimulator:
    """
    Digital Twin Simulation Engine.
    Executes proposed actions on a cloned network model state to predict outcomes.
    """
    def simulate_action(self, telemetry_data, action_plan):
        simulated_state = copy.deepcopy(telemetry_data)
        action_id = action_plan.get("action_id")

        if action_id == "ACT-REROUTE-01":
            for n in simulated_state:
                if n["id"] == "edge-02":
                    n["status"] = "HEALTHY"
                    n["latency"] = 18
                    n["loss"] = 0.0
            return {
                "simulated_nodes": simulated_state,
                "predicted_outcome": "Link failover successful. Latency reduced from 999ms to 18ms. No secondary overload.",
                "cascading_risk": False
            }

        elif action_id == "ACT-REBOOT-CORE":
            # REBOOTING CORE CAUSES TOTAL OUTAGE
            for n in simulated_state:
                n["status"] = "CRITICAL"
                n["loss"] = 100.0
                n["cpu"] = 0
            return {
                "simulated_nodes": simulated_state,
                "predicted_outcome": "CRITICAL FAILURE: Hard reboot of single core router brings down 100% of network traffic trunks.",
                "cascading_risk": True
            }

        elif action_id == "ACT-QOS-02":
            for n in simulated_state:
                if n["id"] == "dist-01":
                    n["cpu"] = 38
                    n["status"] = "HEALTHY"
                if n["id"] == "core-01":
                    n["cpu"] = 25
                    n["status"] = "HEALTHY"
            return {
                "simulated_nodes": simulated_state,
                "predicted_outcome": "Congestion cleared. Dist-01 CPU dropped from 98% to 38%.",
                "cascading_risk": False
            }

        elif action_id == "ACT-ISOLATE-03":
            for n in simulated_state:
                if n["id"] == "host-unreg":
                    n["bw"] = 0
                    n["status"] = "OFFLINE"
                if n["id"] == "edge-02":
                    n["cpu"] = 22
                    n["status"] = "HEALTHY"
            return {
                "simulated_nodes": simulated_state,
                "predicted_outcome": "Threat quarantined. Edge-02 CPU drops to baseline (22%). Integrity restored.",
                "cascading_risk": False
            }

        return {
            "simulated_nodes": simulated_state,
            "predicted_outcome": "Baseline operational parameters maintained.",
            "cascading_risk": False
        }