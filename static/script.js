const form = document.getElementById("reading-form");
const message = document.getElementById("message");
const table = document.getElementById("readings-table");
const summary = document.getElementById("summary");
const priceInput = document.getElementById("price");
const baseFeeInput = document.getElementById("base-fee");

const number = (value, digits = 1) =>
    value.toLocaleString("de-DE", { minimumFractionDigits: digits, maximumFractionDigits: digits });

function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;
}

async function loadReadings() {
    const response = await fetch("/api/readings");
    const readings = await response.json();

    table.innerHTML = "";
    for (const reading of readings) {
        const row = document.createElement("tr");
        const date = new Date(reading.reading_date).toLocaleDateString("de-DE");
        row.innerHTML = `
            <td>${date}</td>
            <td>${number(reading.value_kwh)} kWh</td>
            <td><button class="delete-button" data-id="${reading.id}">Löschen</button></td>`;
        table.appendChild(row);
    }
}

async function loadSummary() {
    const params = new URLSearchParams({ price_ct: priceInput.value, base_fee: baseFeeInput.value });
    const response = await fetch(`/api/summary?${params}`);
    const data = await response.json();

    if (!response.ok) {
        summary.textContent = data.detail;
        return;
    }

    summary.innerHTML = `
        <div class="summary-item"><span>Verbrauch (${data.period_days} Tage)</span><strong>${number(data.consumption_kwh)} kWh</strong></div>
        <div class="summary-item"><span>Pro Tag</span><strong>${number(data.average_per_day_kwh, 2)} kWh</strong></div>
        <div class="summary-item"><span>Hochrechnung Jahr</span><strong>${number(data.forecast_year_kwh, 0)} kWh</strong></div>
        <div class="summary-item"><span>Kosten pro Jahr</span><strong>${number(data.forecast_year_cost_eur, 2)} €</strong></div>
        <div class="summary-item"><span>Empfohlener Abschlag</span><strong>${data.monthly_advance_eur} € / Monat</strong></div>`;
}

async function refresh() {
    await loadReadings();
    await loadSummary();
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const body = {
        reading_date: document.getElementById("reading-date").value,
        value_kwh: parseFloat(document.getElementById("reading-value").value),
    };

    const response = await fetch("/api/readings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    if (response.ok) {
        showMessage("Zählerstand gespeichert.", "success");
        form.reset();
        refresh();
    } else {
        const error = await response.json();
        showMessage(typeof error.detail === "string" ? error.detail : "Bitte die Eingaben prüfen.", "error");
    }
});

table.addEventListener("click", async (event) => {
    if (!event.target.classList.contains("delete-button")) return;
    await fetch(`/api/readings/${event.target.dataset.id}`, { method: "DELETE" });
    refresh();
});

priceInput.addEventListener("change", loadSummary);
baseFeeInput.addEventListener("change", loadSummary);

refresh();
