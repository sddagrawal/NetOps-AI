let networkVis = null;
let chartBw = null;
let chartLat = null;

document.addEventListener('DOMContentLoaded', () => {
    initTopology();
    initCharts();

    document.getElementById('inject-btn').addEventListener('click', () => {
        const scenario = document.getElementById('scenario-select').value;
        runPipeline(scenario);
    });
});

function initTopology() {
    fetch('/api/topology')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('topology-canvas');
            const nodes = data.nodes.map(n => ({
                id: n.id,
                label: `${n.label}\nCPU: 20%`,
                shape: n.type === 'core' ? 'hexagon' : (n.type === 'server' ? 'database' : 'dot'),
                color: { background: '#10b981', border: '#232d42' },
                font: { color: '#e2e8f0', size: 11 }
            }));

            const edges = data.edges.map(e => ({
                from: e.from,
                to: e.to,
                color: { color: '#334155' }
            }));

            networkVis = new vis.Network(container, { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) }, { physics: { enabled: true } });
        });
}

function initCharts() {
    const ctxBw = document.getElementById('chart-bandwidth').getContext('2d');
    chartBw = new Chart(ctxBw, {
        type: 'line',
        data: {
            labels: ['-10s', '-8s', '-6s', '-4s', '-2s', 'Now'],
            datasets: [{ label: 'Core-01 Throughput (Mbps)', data: [300, 310, 305, 300, 315, 300], borderColor: '#00bceb', fill: false }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    const ctxLat = document.getElementById('chart-latency').getContext('2d');
    chartLat = new Chart(ctxLat, {
        type: 'bar',
        data: {
            labels: ['Core-01', 'Dist-01', 'Dist-02', 'Edge-01', 'Edge-02'],
            datasets: [{ label: 'Latency (ms)', data: [10, 10, 10, 10, 10], backgroundColor: '#10b981' }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
}

function runPipeline(scenario) {
    fetch('/api/process_scenario', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario })
    })
    .then(res => res.json())
    .then(res => {
        updateUI(res);
    });
}

function updateUI(res) {
    // 1. Update Topology
    res.telemetry.forEach(n => {
        let color = '#10b981';
        if (n.status === 'DEGRADED') color = '#f59e0b';
        if (n.status === 'CRITICAL') color = '#ef4444';

        try {
            networkVis.body.data.nodes.update({
                id: n.id,
                label: `${n.label}\nCPU: ${n.cpu}%`,
                color: { background: color }
            });
        } catch(e){}
    });

    // 2. Update Root Cause Display
    const rcaBox = document.getElementById('rca-content');
    rcaBox.innerHTML = `
        <span class="badge ${res.root_cause.root_cause_device !== 'None' ? 'badge-critical' : 'badge-healthy'}">
            ${res.root_cause.root_cause_device !== 'None' ? 'Root Cause Identified' : 'System Normal'}
        </span>
        <div style="font-weight:700; color:#38bdf8; margin-top:6px;">${res.root_cause.root_cause_device}</div>
        <p style="font-size:0.75rem; margin-top:4px;">${res.root_cause.explanation}</p>`;

    // 3. Security Classification Display
    const secBox = document.getElementById('classification-content');
    secBox.innerHTML = `
        <span class="badge badge-security">${res.security_classification.category}</span>
        <p style="font-size:0.75rem; margin-top:4px;">${res.security_classification.explanation}</p>`;

    // 4. Proposed Action & Simulation Display
    const actBox = document.getElementById('action-content');
    actBox.innerHTML = `
        <div style="font-weight:600; font-size:0.8rem;">${res.action_plan.name}</div>
        <p style="font-size:0.75rem; margin-top:4px; color:var(--text-muted);"><b>Sim Outcome:</b> ${res.simulation.predicted_outcome}</p>`;

    // 5. Final Decision Display
    const decBox = document.getElementById('decision-container');
    const dec = res.final_decision;
    decBox.innerHTML = `
        <div class="decision-banner ${dec.banner_class}">
            <div style="font-weight:700;">DECISION: ${dec.decision}</div>
            <div style="font-size:0.75rem; margin-top:4px;">${dec.reason}</div>
        </div>`;
}