class DecisionEngine:
    """
    Synthesizes safety evaluation and simulation results into the final decision state:
    AUTO-EXECUTE | HUMAN APPROVAL REQUIRED | REJECT
    """
    def make_decision(self, safety_eval):
        status = safety_eval["safety_status"]

        if status == "REJECTED":
            return {
                "decision": "REJECT",
                "banner_class": "decision-REJECT",
                "reason": safety_eval["reason"]
            }
        elif status == "REQUIRES_HUMAN_APPROVAL":
            return {
                "decision": "HUMAN-APPROVAL-REQUIRED",
                "banner_class": "decision-HUMAN-APPROVAL-REQUIRED",
                "reason": safety_eval["reason"]
            }
        else:
            return {
                "decision": "AUTO-EXECUTE",
                "banner_class": "decision-AUTO-EXECUTE",
                "reason": safety_eval["reason"]
            }