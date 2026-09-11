class SecurityClassifier:
    """
    Classifies events into Operational Failures vs. Potential Security Incidents.
    """
    def classify(self, scenario, root_cause_info):
        if scenario == "SECURITY_EVENT":
            return {
                "category": "POTENTIAL SECURITY EVENT",
                "risk_level": "HIGH",
                "explanation": "Unregistered endpoint (Host-03) generating excessive outbound connections. Signature matches Data Exfiltration.",
                "human_investigation_recommended": True
            }
        elif scenario == "LEGITIMATE_SURGE":
            return {
                "category": "OPERATIONAL (FALSE POSITIVE SECURITY ALERT)",
                "risk_level": "LOW",
                "explanation": "High volume egress validated against system crontab DB Sync window.",
                "human_investigation_recommended": False
            }
        else:
            return {
                "category": "OPERATIONAL FAILURE / DEGRADATION",
                "risk_level": "MEDIUM" if root_cause_info["root_cause_device"] != "None" else "NONE",
                "explanation": "Performance degradation due to traffic load or hardware failure.",
                "human_investigation_recommended": False
            }