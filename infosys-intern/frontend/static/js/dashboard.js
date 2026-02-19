async function loadDashboard() {

    try {
        const response = await fetch("/api/trends");
        const data = await response.json();

        console.log("Trend Data:", data);

        // ================================
        // EXTRACT TOP 5 COMPARISON DATA
        // ================================
        const materials = data.comparison.map(item => item.material_name);
        const costs = data.comparison.map(item => item.cost_rupees);
        const co2Scores = data.comparison.map(item => item.co2_score);
        const suitabilityScores = data.comparison.map(item => item.suitability_score);

        // ================================
        // EXTRACT USAGE TREND
        // ================================
        const usageMaterials = data.usage_trend.map(item => item.material_name);
        const usageCounts = data.usage_trend.map(item => item.count);

        // ================================
        // COST CHART
        // ================================
        new Chart(document.getElementById("costChart"), {
            type: "bar",
            data: {
                labels: materials,
                datasets: [{
                    label: "Cost (₹)",
                    data: costs
                }]
            }
        });

        // ================================
        // CO2 CHART
        // ================================
        new Chart(document.getElementById("co2Chart"), {
            type: "bar",
            data: {
                labels: materials,
                datasets: [{
                    label: "CO2 Score",
                    data: co2Scores
                }]
            }
        });

        // ================================
        // SUITABILITY CHART
        // ================================
        new Chart(document.getElementById("suitabilityChart"), {
            type: "line",
            data: {
                labels: materials,
                datasets: [{
                    label: "Suitability Score",
                    data: suitabilityScores
                }]
            }
        });

        // ================================
        // MATERIAL USAGE TREND
        // ================================
        new Chart(document.getElementById("usageChart"), {
            type: "bar",
            data: {
                labels: usageMaterials,
                datasets: [{
                    label: "Usage Count",
                    data: usageCounts
                }]
            }
        });

    } catch (error) {
        console.error("Dashboard Error:", error);
        alert("Failed to load dashboard data.");
    }
}

loadDashboard();
