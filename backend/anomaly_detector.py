class AnomalyDetector:
    """
    Explainable Rule-Based Anomaly Detection Engine.
    Evaluates telemetry against defined operational baseline thresholds.
    """
    CPU_THRESHOLD = 80.0
    LOSS_THRESHOLD = 2.0
    LATENCY_THRESHOLD = 50.0

    def analyze(self, telemetry_data):
        anomalies = []
        for node in telemetry_data:
            node_id = node["id"]
            node_label = node["label"]

            if node["cpu"] > self.CPU_THRESHOLD:
                anomalies.append({
                    "device": node_id,
                    "label": node_label,
                    "metric": "CPU Utilization",
                    "value": f"{node['cpu']}%",
                    "severity": "CRITICAL" if node["cpu"] > 90 else "HIGH"
                })
            
            if node["loss"] > self.LOSS_THRESHOLD:
                anomalies.append({
                    "device": node_id,
                    "label": node_label,
                    "metric": "Packet Loss",
                    "value": f"{node['loss']}%",
                    "severity": "CRITICAL"
                })

            if node["latency"] > self.LATENCY_THRESHOLD and node["latency"] != 999:
                anomalies.append({
                    "device": node_id,
                    "label": node_label,
                    "metric": "High Latency",
                    "value": f"{node['latency']} ms",
                    "severity": "HIGH"
                })

        return anomalies