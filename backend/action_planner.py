class ActionPlanner:
    """
    Generates candidate remediation plans for the identified root cause.
    """
    def generate_plans(self, scenario):
        if scenario == "SINGLE_FAILURE":
            return {
                "action_id": "ACT-REROUTE-01",
                "name": "Dynamic Path Failover to Dist-Router-02",
                "target_device": "Dist-Router-02",
                "expected_benefit": "Restores connectivity to isolated segment via alternate trunk.",
                "reversible": True
            }
        elif scenario == "CASCADING_CONGESTION":
            return {
                "action_id": "ACT-QOS-02",
                "name": "Apply Ingress Rate-Limiting ACL (QoS 50Mbps)",
                "target_device": "Edge-Router-01",
                "expected_benefit": "Eliminates Dist-01 buffer overflow and clears core backpressure.",
                "reversible": True
            }
        elif scenario == "SECURITY_EVENT":
            return {
                "action_id": "ACT-ISOLATE-03",
                "name": "Quarantine Host-03 & Apply Null-Route ACL",
                "target_device": "Edge-Router-02",
                "expected_benefit": "Immediately halts outbound exfiltration path.",
                "reversible": True
            }
        elif scenario == "UNSAFE_REMEDIATION":
            return {
                "action_id": "ACT-REBOOT-CORE",
                "name": "Hard Restart Core-Router-01 Operating System",
                "target_device": "Core-Router-01",
                "expected_benefit": "Clears memory leak context.",
                "reversible": False
            }
        else: # Default/Normal
            return {
                "action_id": "ACT-NOOP",
                "name": "Maintain Active Monitoring",
                "target_device": "None",
                "expected_benefit": "No action required.",
                "reversible": True
            }