document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("recommendationForm");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const formData = new FormData(this);

        const data = {
            product_type: formData.get("product_type"),
            product_category: formData.get("product_category"),
            fragility: formData.get("fragility"),
            shipping_type: formData.get("shipping_type"),
            sustainability_priority: formData.get("sustainability_priority")
        };

        console.log("Sending:", data);

        const tableBody = document.querySelector("#resultsTable tbody");
        tableBody.innerHTML = "";

        // Hide summary initially
        document.getElementById("predictionSummary").style.display = "none";

        try {

            const response = await fetch("/api/ranking", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error("Server returned error: " + response.status);
            }

            const result = await response.json();
            console.log("Received:", result);

            // Check correct backend format
            if (!result.ranking || result.ranking.length === 0) {

                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="text-center text-danger">
                            No suitable materials found
                        </td>
                    </tr>
                `;
                return;
            }

            let avgCost = 0;
            let avgCO2 = 0;
            let avgSuit = 0;

            result.ranking.forEach((item, index) => {

                const cost = Number(item.cost_rupees) || 0;
                const co2 = Number(item.co2_score) || 0;
                const suit = Number(item.suitability_score) || 0;
                const finalScore = Number(item.final_score) || 0;

                avgCost += cost;
                avgCO2 += co2;
                avgSuit += suit;

                const row = `
                    <tr>
                        <td>${item.rank || index + 1}</td>
                        <td>${item.material_name}</td>
                        <td>${cost.toFixed(2)}</td>
                        <td>${co2.toFixed(2)}</td>
                        <td>${suit.toFixed(2)}</td>
                        <td>${finalScore.toFixed(3)}</td>
                    </tr>
                `;

                tableBody.insertAdjacentHTML("beforeend", row);
            });

            // Calculate averages
            avgCost /= result.ranking.length;
            avgCO2 /= result.ranking.length;
            avgSuit /= result.ranking.length;

            // Update summary
            document.getElementById("predCost").innerText =
                "₹ " + avgCost.toFixed(2);

            document.getElementById("predCO2").innerText =
                avgCO2.toFixed(2);

            document.getElementById("predSuit").innerText =
                avgSuit.toFixed(2);

            document.getElementById("predictionSummary").style.display = "flex";

        } catch (error) {

            console.error("API ERROR:", error);

            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-danger">
                        Failed to load recommendations. Check backend.
                    </td>
                </tr>
            `;
        }
    });

});
