// app.js
document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // DASHBOARD: Load Charts
    // ================================
    async function loadDashboard() {
        try {
            const API_URL = "/api/trends";
            // For separate backend on Render:
            // const API_URL = "https://your-backend.onrender.com/api/trends";

            const response = await fetch(API_URL);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            console.log("Dashboard Data:", data);

            const comparison = data.comparison || [];
            const usageTrend = data.usage_trend || [];

            if (comparison.length === 0 && usageTrend.length === 0) {
                console.warn("No dashboard data found.");
                return;
            }

            const materials = comparison.map(item => item.material_name || "N/A");
            const costs = comparison.map(item => item.cost_rupees || 0);
            const co2Scores = comparison.map(item => item.co2_score || 0);
            const suitabilityScores = comparison.map(item => item.suitability_score || 0);

            const usageMaterials = usageTrend.map(item => item.material_name || "N/A");
            const usageCounts = usageTrend.map(item => item.count || 0);

            function createChart(ctxId, type, labels, datasetLabel, data, color = "rgba(54, 162, 235, 0.6)") {
                const ctx = document.getElementById(ctxId);
                if (!ctx) return console.warn(`Canvas element '${ctxId}' not found.`);
                new Chart(ctx, {
                    type: type,
                    data: {
                        labels: labels,
                        datasets: [{
                            label: datasetLabel,
                            data: data,
                            backgroundColor: color,
                            borderColor: color.replace("0.6", "1"),
                            borderWidth: 1,
                            fill: type === "line" ? false : true
                        }]
                    },
                    options: { responsive: true, scales: { y: { beginAtZero: true } } }
                });
            }

            createChart("costChart", "bar", materials, "Cost (₹)", costs, "rgba(255, 99, 132, 0.6)");
            createChart("co2Chart", "bar", materials, "CO2 Score", co2Scores, "rgba(54, 162, 235, 0.6)");
            createChart("suitabilityChart", "line", materials, "Suitability Score", suitabilityScores, "rgba(75, 192, 192, 0.6)");
            createChart("usageChart", "bar", usageMaterials, "Usage Count", usageCounts, "rgba(153, 102, 255, 0.6)");

        } catch (error) {
            console.error("Dashboard Error:", error);
        }
    }

    loadDashboard();

    // ================================
    // FORM: Material Recommendation
    // ================================
    const form = document.getElementById("recommendationForm");
    const tableBody = document.querySelector("#resultsTable tbody");
    const summaryDiv = document.getElementById("predictionSummary");

    if (!form || !tableBody || !summaryDiv) {
        console.error("Form or table or summary div not found.");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const data = {
            product_type: formData.get("product_type") || "",
            product_category: formData.get("product_category") || "",
            fragility: formData.get("fragility") || "",
            shipping_type: formData.get("shipping_type") || "",
            sustainability_priority: formData.get("sustainability_priority") || ""
        };

        console.log("Sending Recommendation Data:", data);

        tableBody.innerHTML = "";
        summaryDiv.style.display = "none";

        try {
            const API_URL = "/api/ranking";
            // For separate backend on Render:
            // const API_URL = "https://your-backend.onrender.com/api/ranking";

            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error("Server error: " + response.status);

            const result = await response.json();
            console.log("Recommendation Result:", result);

            const ranking = result.ranking || [];
            if (!Array.isArray(ranking) || ranking.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">No suitable materials found.</td></tr>`;
                return;
            }

            let totalCost = 0, totalCO2 = 0, totalSuit = 0;

            ranking.forEach((item, index) => {
                const cost = Number(item.cost_rupees) || 0;
                const co2 = Number(item.co2_score) || 0;
                const suit = Number(item.suitability_score) || 0;
                const finalScore = Number(item.final_score) || 0;

                totalCost += cost;
                totalCO2 += co2;
                totalSuit += suit;

                const row = `
                    <tr>
                        <td>${item.rank || index + 1}</td>
                        <td>${item.material_name || "N/A"}</td>
                        <td>${cost.toFixed(2)}</td>
                        <td>${co2.toFixed(2)}</td>
                        <td>${suit.toFixed(2)}</td>
                        <td>${finalScore.toFixed(3)}</td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML("beforeend", row);
            });

            document.getElementById("predCost").innerText = "₹ " + (totalCost / ranking.length).toFixed(2);
            document.getElementById("predCO2").innerText = (totalCO2 / ranking.length).toFixed(2);
            document.getElementById("predSuit").innerText = (totalSuit / ranking.length).toFixed(2);
            summaryDiv.style.display = "flex";

        } catch (error) {
            console.error("Recommendation API Error:", error);
            tableBody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Failed to load recommendations. Check backend.</td></tr>`;
        }
    });

});