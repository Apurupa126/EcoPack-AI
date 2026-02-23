// dashboard.js
document.addEventListener("DOMContentLoaded", function () {

    async function loadDashboard() {

        try {

            const response = await fetch("/api/trends");

            if (!response.ok) {
                throw new Error("HTTP error " + response.status);
            }

            const data = await response.json();

            console.log("Dashboard API Data:", data);

            const comparison = data.comparison || [];
            const usageTrend = data.usage_trend || [];

            if (comparison.length === 0) {
                console.warn("No comparison data received");
                return;
            }

            const materials = comparison.map(x => x.material_name);
            const costs = comparison.map(x => Number(x.cost_rupees));
            const co2 = comparison.map(x => Number(x.co2_score));
            const suit = comparison.map(x => Number(x.suitability_score));

            const usageMaterials = usageTrend.map(x => x.material_name);
            const usageCounts = usageTrend.map(x => Number(x.count));

            createChart("costChart", "bar", materials, "Cost (₹)", costs);
            createChart("co2Chart", "bar", materials, "CO₂ Score", co2);
            createChart("suitabilityChart", "line", materials, "Suitability Score", suit);
            createChart("usageChart", "bar", usageMaterials, "Usage Count", usageCounts);

        } catch (err) {
            console.error("Dashboard Load Failed:", err);
        }
    }

    function createChart(id, type, labels, label, data) {

        const ctx = document.getElementById(id);
        if (!ctx) return;

        new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderWidth: 1,
                    fill: type === "line" ? false : true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    loadDashboard();

});