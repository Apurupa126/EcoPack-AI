// main.js
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("recommendationForm");
    const tableBody = document.querySelector("#resultsTable tbody");
    const summaryDiv = document.getElementById("predictionSummary");
    const submitBtn = document.getElementById("submitBtn");

    const topContainer = document.getElementById("topMaterialsContainer");
    const topSection = document.getElementById("topRecommendations");

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        submitBtn.innerHTML = "Analyzing...";
        submitBtn.disabled = true;

        const formData = new FormData(this);

        const data = {
            product_type: formData.get("product_type"),
            product_category: formData.get("product_category"),
            fragility: formData.get("fragility"),
            shipping_type: formData.get("shipping_type"),
            sustainability_priority: formData.get("sustainability_priority")
        };

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
                throw new Error("Server error");
            }

            const result = await response.json();
            const ranking = result.ranking;

            if (!ranking || ranking.length === 0) {
                tableBody.innerHTML =
                `<tr><td colspan="6" class="text-danger text-center">
                No suitable materials found</td></tr>`;
                resetButton();
                return;
            }

            let totalCost = 0;
            let totalCO2 = 0;
            let totalSuit = 0;

            // ================= TOP 3 MATERIAL CARDS =================
            ranking.slice(0,3).forEach((item,index)=>{

                let badge="";
                let rankClass="";

                if(item.rank==1){
                    badge='<span class="badge-gold">🥇 Best Choice</span>';
                    rankClass="rank-1";
                }
                else if(item.rank==2){
                    badge='<span class="badge-silver">🥈 Second</span>';
                    rankClass="rank-2";
                }
                else if(item.rank==3){
                    badge='<span class="badge-bronze">🥉 Third</span>';
                    rankClass="rank-3";
                }

                const card = `
                <div class="col-md-4 mb-4">
                    <div class="material-card ${rankClass}">
                        ${badge}
                        <h5 class="mt-2">Rank #${item.rank}</h5>
                        <h6>${item.material_name}</h6>
                        ₹ ${Number(item.cost_rupees).toFixed(2)} <br>
                        CO₂ ${Number(item.co2_score).toFixed(2)} <br>
                        Suit ${Number(item.suitability_score).toFixed(2)} <br>
                        Score ${Number(item.final_score).toFixed(3)}
                    </div>
                </div>`;

                topContainer.insertAdjacentHTML("beforeend", card);
            });

            topSection.style.display="block";

            // ================= TABLE RANK COLORS =================
            ranking.forEach(item=>{

                let rowClass="";
                let medal="";

                if(item.rank==1){
                    rowClass="rank-1";
                    medal="🥇";
                }
                else if(item.rank==2){
                    rowClass="rank-2";
                    medal="🥈";
                }
                else if(item.rank==3){
                    rowClass="rank-3";
                    medal="🥉";
                }

                totalCost += Number(item.cost_rupees);
                totalCO2 += Number(item.co2_score);
                totalSuit += Number(item.suitability_score);

                const row = `
                <tr class="${rowClass}">
                    <td>${medal} ${item.rank}</td>
                    <td>${item.material_name}</td>
                    <td>${Number(item.cost_rupees).toFixed(2)}</td>
                    <td>${Number(item.co2_score).toFixed(2)}</td>
                    <td>${Number(item.suitability_score).toFixed(2)}</td>
                    <td>${Number(item.final_score).toFixed(3)}</td>
                </tr>`;

                tableBody.insertAdjacentHTML("beforeend",row);
            });

            document.getElementById("predCost").innerText =
            "₹ "+(totalCost/ranking.length).toFixed(2);

            document.getElementById("predCO2").innerText =
            (totalCO2/ranking.length).toFixed(2);

            document.getElementById("predSuit").innerText =
            (totalSuit/ranking.length).toFixed(2);

            summaryDiv.style.display="flex";

            resetButton();

        } catch(err){

            console.error("Ranking Failed:",err);

            tableBody.innerHTML =
            `<tr><td colspan="6" class="text-danger text-center">
            Failed to load recommendations</td></tr>`;

            resetButton();
        }
    });

    function resetButton(){
        submitBtn.innerHTML="Get AI Recommendations";
        submitBtn.disabled=false;
    }

});