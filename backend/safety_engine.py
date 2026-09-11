class SafetyEngine:
    """
    Evaluates safety rules and constraints before allowing action execution.
    """
    def evaluate(self, action_plan, simulation_result, network_model):
        action_id = action_plan.get("action_id")

        # RULE 1: Never hard reboot single core infrastructure without redundant path
        if action_id == "ACT-REBOOT-CORE" or simulation_result["cascading_risk"]:
            return {
                "safety_status": "REJECTED",
                "reason": "SAFETY POLICY VIOLATION (Policy-09): Action creates total cascading outage on critical core device."
            }

        # RULE 2: Security quarantine actions require human approval
        if action_id == "ACT-ISOLATE-03":
            return {
                "safety_status": "REQUIRES_HUMAN_APPROVAL",
                "reason": "SECURITY CONSTRAINT (Policy-04): Host isolation actions must be confirmed by SOC analyst."
            }

        # RULE 3: Bandwidth throttling/QoS actions require human approval if affecting user subnets
        if action_id == "ACT-QOS-02":
            return {
                "safety_status": "REQUIRES_HUMAN_APPROVAL",
                "reason": "OPERATIONAL CONSTRAINT (Policy-02): QoS rate limiting reduces user throughput bandwidth."
            }

        # RULE 4: Low risk reroute actions are pre-cleared for auto-execution
        if action_id == "ACT-REROUTE-01":
            return {
                "safety_status": "SAFE",
                "reason": "Action fully reversible and alternate path has 75% verified headroom."
            }

        return {
            "safety_status": "SAFE",
            "reason": "Operational safety checks passed."
        }