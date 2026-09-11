import copy

class TelemetryEngine:
    """
    Generates realistic telemetry streams for each node based on the active scenario.
    """
    def __init__(self, network_model):
        self.net = network_model

    def get_telemetry(self, scenario):
        nodes = copy.deepcopy(self.net.get_topology_dict()["nodes"])
        
        # Default Healthy Telemetry State
        for n in nodes:
            n["cpu"] = 20
            n["bw"] = 30
            n["latency"] = 10
            n["loss"] = 0.0
            n["status"] = "HEALTHY"

        if scenario == "SINGLE_FAILURE":
            for n in nodes:
                if n["id"] == "edge-02":
                    n["status"] = "CRITICAL"
                    n["cpu"] = 0
                    n["loss"] = 100.0
                    n["latency"] = 999

        elif scenario == "CORE_OVERLOAD":
            for n in nodes:
                if n["id"] == "core-01":
                    n["status"] = "CRITICAL"
                    n["cpu"] = 96
                    n["bw"] = 920
                    n["latency"] = 145
                    n["loss"] = 12.5

        elif scenario == "CASCADING_CONGESTION":
            for n in nodes:
                if n["id"] == "dist-01":
                    n["status"] = "CRITICAL"
                    n["cpu"] = 98
                    n["bw"] = 490
                elif n["id"] == "core-01":
                    n["status"] = "DEGRADED"
                    n["cpu"] = 82
                    n["latency"] = 65

        elif scenario == "SECURITY_EVENT":
            for n in nodes:
                if n["id"] == "host-unreg":
                    n["status"] = "CRITICAL"
                    n["bw"] = 95
                elif n["id"] == "edge-02":
                    n["status"] = "DEGRADED"
                    n["cpu"] = 88
                    n["bw"] = 195

        elif scenario == "LEGITIMATE_SURGE":
            for n in nodes:
                if n["id"] == "srv-db":
                    n["status"] = "DEGRADED"
                    n["cpu"] = 85
                    n["bw"] = 750

        elif scenario == "UNSAFE_REMEDIATION":
            for n in nodes:
                if n["id"] == "core-01":
                    n["status"] = "CRITICAL"
                    n["cpu"] = 92
                    n["loss"] = 8.5

        return nodes