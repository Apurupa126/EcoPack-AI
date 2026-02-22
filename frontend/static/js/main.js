// main.js
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("recommendationForm");
    const tableBody = document.querySelector("#resultsTable tbody");
    const summaryDiv = document.getElementById("predictionSummary");
    const submitBtn = document.getElementById("submitBtn");

    const topContainer = document.getElementById("topMaterialsContainer");
    const topSection = document.getElementById("topRecommendations");

    if (!form || !tableBody || !summaryDiv) {
        console.error("Required elements not found in HTML.");
        return;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        // Loading state
        submitBtn.innerHTML = "Analyzing...";
        submitBtn.disabled = true;

        // Collect form data
        const formData = new FormData(this);
        const data = {
            product_type: formData.get("product_type") || "",
            product_category: formData.get("product_category") || "",
            fragility: formData.get("fragility") || "",
            shipping_type: formData.get("shipping_type") || "",
            sustainability_priority: formData.get("sustainability_priority") || ""
        };

        // Clear previous results
        tableBody.innerHTML = "";
        summaryDiv.style.display = "none";
        topContainer.innerHTML = "";
        topSection.style.display = "none";

        try {
            const response = await fetch("/api/ranking", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error("Server error: " + response.status);
            }

            const result = await response.json();
            const ranking = result.ranking || [];

            if (!Array.isArray(ranking) || ranking.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center text-danger">
                            No suitable materials found.
                        </td>
                    </tr>
                `;
                resetButton();
                return;
            }

            let totalCost = 0,
                totalCO2 = 0,
                totalSuit = 0;

            /* ==============================
               TOP 3 MATERIAL CARDS
            ===============================*/
            ranking.slice(0, 3).forEach((item, index) => {

                let borderClass = "";
                let medalIcon = "";

                if (index === 0) {
                    borderClass = "gold-border";
                    medalIcon = "🥇";
                }
                if (index === 1) {
                    borderClass = "silver-border";
                    medalIcon = "🥈";
                }
                if (index === 2) {
                    borderClass = "bronze-border";
                    medalIcon = "🥉";
                }

                const card = `
                    <div class="col-md-4 mb-4">
                        <div class="material-card ${borderClass}" style="animation-delay:${index * 0.2}s">
                            <div class="material-rank">${medalIcon} Rank #${item.rank || index + 1}</div>
                            <div class="material-title mt-2">${item.material_name || "N/A"}</div>

                            <div class="mt-3">
                                💰 Cost: ₹ ${Number(item.cost_rupees).toFixed(2)} <br>
                                🌍 CO₂ Score: ${Number(item.co2_score).toFixed(2)} <br>
                                📦 Suitability: ${Number(item.suitability_score).toFixed(2)} <br>
                                ⭐ Final Score: ${Number(item.final_score).toFixed(3)}
                            </div>
                        </div>
                    </div>
                `;

                topContainer.insertAdjacentHTML("beforeend", card);
            });

            topSection.style.display = "block";

            /* ==============================
               FULL TABLE RANKING
            ===============================*/
            ranking.forEach((item, index) => {

                const cost = Number(item.cost_rupees) || 0;
                const co2 = Number(item.co2_score) || 0;
                const suit = Number(item.suitability_score) || 0;
                const finalScore = Number(item.final_score) || 0;

                totalCost += cost;
                totalCO2 += co2;
                totalSuit += suit;

                const isTop = index === 0
                    ? "style='background:#E8F5E9;font-weight:600;'"
                    : "";

                const row = `
                    <tr ${isTop}>
                        <td>${item.rank || index + 1}</td>
                        <td>${item.material_name || "N/A"}</td>
                        <td>₹ ${cost.toFixed(2)}</td>
                        <td>${co2.toFixed(2)}</td>
                        <td>${suit.toFixed(2)}</td>
                        <td>${finalScore.toFixed(3)}</td>
                    </tr>
                `;

                tableBody.insertAdjacentHTML("beforeend", row);
            });

            /* ==============================
               KPI SUMMARY (AVERAGE)
            ===============================*/
            document.getElementById("predCost").innerText =
                "₹ " + (totalCost / ranking.length).toFixed(2);

            document.getElementById("predCO2").innerText =
                (totalCO2 / ranking.length).toFixed(2);

            document.getElementById("predSuit").innerText =
                (totalSuit / ranking.length).toFixed(2);

            // Smooth fade-in
            summaryDiv.style.display = "flex";
            summaryDiv.style.opacity = "0";

            setTimeout(() => {
                summaryDiv.style.transition = "opacity 0.6s ease";
                summaryDiv.style.opacity = "1";
            }, 100);

            resetButton();

        } catch (error) {
            console.error("API ERROR:", error);

            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-danger">
                        Failed to load recommendations. Please check backend.
                    </td>
                </tr>
            `;

            resetButton();
        }
    });

    function resetButton() {
        submitBtn.innerHTML = "Get AI Recommendations";
        submitBtn.disabled = false;
    }

});