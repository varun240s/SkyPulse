// Theme Toggle
const themeToggle = document.getElementById("theme-toggle");
const body = document.body;

themeToggle.addEventListener("click", () => {
  body.dataset.theme = body.dataset.theme === "dark" ? "light" : "dark";
});

// Chart Configurations
const chartConfigs = {
  co2: {
    type: "line",
    data: { labels: [], datasets: [{ label: "CO₂ Levels (ppm)", data: [], borderColor: "#e74c3c", fill: false }] },
    options: { responsive: true, scales: { x: { title: { text: "Year" } }, y: { title: { text: "CO₂ (ppm)" } } } }
  },
  temperature: {
    type: "line",
    data: { labels: [], datasets: [{ label: "Temperature (°C)", data: [], borderColor: "#f1c40f", fill: false }, { label: "Temperature Trend", data: [], borderColor: "#e67e22", borderDash: [5, 5], fill: false }] },
    options: { responsive: true, scales: { x: { title: { text: "Year" } }, y: { title: { text: "Temperature (°C)" } } } }
  },
  deforestation: {
    type: "line",
    data: { labels: [], datasets: [{ label: "Forest Area (sq. km)", data: [], borderColor: "#27ae60", fill: false }] },
    options: { responsive: true, scales: { x: { title: { text: "Year" } }, y: { title: { text: "Area (sq. km)" } } } }
  },
  seaLevel: {
    type: "line",
    data: { labels: [], datasets: [{ label: "Sea Level (mm)", data: [], borderColor: "#3498db", fill: false }] },
    options: { responsive: true, scales: { x: { title: { text: "Year" } }, y: { title: { text: "Sea Level (mm)" } } } }
  }
};

// Initialize Charts
const charts = {
  co2: new Chart(document.getElementById("co2Chart"), chartConfigs.co2),
  temperature: new Chart(document.getElementById("temperatureChart"), chartConfigs.temperature),
  deforestation: new Chart(document.getElementById("deforestationChart"), chartConfigs.deforestation),
  seaLevel: new Chart(document.getElementById("seaLevelChart"), chartConfigs.seaLevel)
};

// Function to Calculate Yearly Mean Values
function calculateYearlyMean(data, valueKey) {
  const yearlyData = {};

  data.forEach(entry => {
    const year = new Date(entry.Date).getFullYear();
    const value = parseFloat(entry[valueKey]);

    if (!yearlyData[year]) yearlyData[year] = { sum: 0, count: 0 };
    yearlyData[year].sum += value;
    yearlyData[year].count += 1;
  });

  return Object.keys(yearlyData).map(year => ({
    year: parseInt(year),
    meanValue: yearlyData[year].sum / yearlyData[year].count
  }));
}

// Function to Calculate Linear Regression (For Temperature Trend)
function calculateTrend(data) {
  const x = data.map((_, i) => i);
  const y = data;
  const n = x.length;

  const sumX = x.reduce((a, b) => a + b, 0);
  const sumY = y.reduce((a, b) => a + b, 0);
  const sumXY = x.reduce((a, _, i) => a + x[i] * y[i], 0);
  const sumXX = x.reduce((a, _, i) => a + x[i] * x[i], 0);

  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;

  return y.map((_, i) => intercept + slope * i);
}

// Fetch and Update Data
async function fetchAndUpdateData() {
  try {
    // Fetch CO2 Data (Yearly Mean)
    const co2Response = await fetch("public/data/predictions/prophet_co2_predictions.json");
    const co2Data = await co2Response.json();
    const yearlyCO2 = calculateYearlyMean(co2Data, "Predicted");
    
    charts.co2.data.labels = yearlyCO2.map(d => d.year);
    charts.co2.data.datasets[0].data = yearlyCO2.map(d => d.meanValue);
    charts.co2.update();

    // Fetch Temperature Data & Calculate Trend
    const tempResponse = await fetch("public/data/processed/decadal_temperature.json");
    const tempData = await tempResponse.json();
    const temperatures = tempData.map(d => d.Temperature);

    charts.temperature.data.labels = tempData.map(d => d.Decade);
    charts.temperature.data.datasets[0].data = temperatures;
    charts.temperature.data.datasets[1].data = calculateTrend(temperatures);
    charts.temperature.update();

    // Fetch Deforestation Data (Keep Raw Data)
    const deforestationResponse = await fetch("public/data/processed/deforestation.json");
    const deforestationData = await deforestationResponse.json();

    charts.deforestation.data.labels = deforestationData.map(d => d.Year);
    charts.deforestation.data.datasets[0].data = deforestationData.map(d => d.Area_Deforested);
    charts.deforestation.update();

    // Fetch Sea Level Data (Yearly Mean)
    const seaLevelResponse = await fetch("public/data/processed/sea_level.json");
    const seaLevelData = await seaLevelResponse.json();
    const yearlySeaLevels = calculateYearlyMean(seaLevelData, "Sea Level");

    charts.seaLevel.data.labels = yearlySeaLevels.map(d => d.year);
    charts.seaLevel.data.datasets[0].data = yearlySeaLevels.map(d => d.meanValue);
    charts.seaLevel.update();

  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Load Data on Page Load
window.addEventListener("load", fetchAndUpdateData);
