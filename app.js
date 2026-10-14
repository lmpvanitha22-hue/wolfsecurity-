/* ============================================================
   Phishing URL Detector — Frontend Logic
   ============================================================ */

const MAX_BATCH_URLS = 1000;

function classifyRisk(pct) {
  if (pct < 35) return "SAFE";
  if (pct < 70) return "SUSPICIOUS";
  return "PHISHING";
}

function verdictIcon(status) {
  return { SAFE: "✅", SUSPICIOUS: "⚠️", PHISHING: "🚨" }[status] ?? "❓";
}

function setBar(barId, pct) {
  const el = document.getElementById(barId);
  // Use setTimeout so CSS transition triggers after element is visible
  setTimeout(() => { el.style.width = Math.min(pct, 100) + "%"; }, 50);
}

function populateReasons(listId, reasons, status) {
  const ul = document.getElementById(listId);
  ul.innerHTML = "";
  reasons.forEach(r => {
    const li = document.createElement("li");
    li.textContent = r;
    li.className = "model-reason-item reason-" + status;
    ul.appendChild(li);
  });
}

async function analyzeUrl() {
  const input  = document.getElementById("urlInput");
  const btn    = document.getElementById("analyzeBtn");
  const btnTxt = document.getElementById("btnText");
  const spin   = document.getElementById("btnSpinner");
  const panel  = document.getElementById("resultPanel");

  const urls = input.value.split(/\r?\n/).map(url => url.trim()).filter(Boolean);
  if (!urls.length) { input.focus(); input.style.borderColor = "#ef4444"; setTimeout(() => input.style.borderColor = "", 1200); return; }
  if (urls.length > MAX_BATCH_URLS) {
    alert(`Analyze up to ${MAX_BATCH_URLS.toLocaleString()} URLs per request.`);
    input.focus();
    return;
  }

  // Loading state
  btn.disabled = true;
  btnTxt.textContent = "Analyzing…";
  spin.classList.remove("hidden");
  panel.classList.add("hidden");
  document.getElementById("batchPanel").classList.add("hidden");

  try {
    const res  = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(urls.length === 1 ? { url: urls[0] } : { urls })
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    if (data.results) renderBatchResults(data);
    else renderResult(data);
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btnTxt.textContent = "Analyze URLs";
    spin.classList.add("hidden");
  }
}

function renderBatchResults(data) {
  const panel = document.getElementById("batchPanel");
  const tbody = document.getElementById("batchResults");
  tbody.replaceChildren();
  document.getElementById("batchHeading").textContent = `Results for ${data.count.toLocaleString()} URLs`;
  const rows = document.createDocumentFragment();

  data.results.forEach(result => {
    const row = document.createElement("tr");
    [result.url, result.status, `${result.risk_score}%`,
      result.lr_prob === null ? "Blacklist" : `${result.lr_status} · ${result.lr_prob}%`,
      result.rf_prob === null ? "Blacklist" : `${result.rf_status} · ${result.rf_prob}%`
    ].forEach((value, index) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      if (index === 1) cell.className = "table-verdict verdict-text-" + result.status;
      row.appendChild(cell);
    });
    rows.appendChild(row);
  });
  tbody.appendChild(rows);

  panel.classList.remove("hidden");
  panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function loadModelMetrics() {
  const body = document.getElementById("metricsBody");
  const method = document.getElementById("metricsMethod");
  const note = document.getElementById("metricsNote");
  try {
    const response = await fetch("/metrics");
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to load model metrics.");
    Object.entries(data.models).forEach(([name, metrics]) => {
      const row = document.createElement("tr");
      [name, metrics.accuracy, metrics.precision, metrics.recall, metrics.f1_score]
        .forEach((value, index) => {
          const cell = document.createElement("td");
          cell.textContent = index === 0 ? value : `${value}%`;
          row.appendChild(cell);
        });
      body.appendChild(row);
    });
    method.textContent = data.evaluation;
    note.textContent = `Scores use phishing as the positive class and are based on ${data.sample_count} synthetic training URLs. Treat this small demo dataset as illustrative, not a measure of production performance.`;
  } catch (error) {
    method.textContent = "Evaluation unavailable";
    note.textContent = error.message;
  }
}

function renderResult(data) {
  const panel = document.getElementById("resultPanel");

  /* --- Overall verdict --- */
  const badge = document.getElementById("verdictBadge");
  badge.className = "verdict-badge verdict-" + data.status;
  document.getElementById("verdictIcon").textContent = verdictIcon(data.status);
  document.getElementById("verdictText").textContent = data.status;

  /* --- Combined score --- */
  document.getElementById("combinedPct").textContent = data.risk_score + "%";
  setBar("combinedBar", data.risk_score);

  /* --- Blacklist path: no per-model data --- */
  const modelsGrid = document.querySelector(".models-grid");
  if (data.lr_prob == null) {
    modelsGrid.style.display = "none";
  } else {
    modelsGrid.style.display = "grid";

    /* LR model */
    const lrStatus = classifyRisk(data.lr_prob);
    document.getElementById("lrPct").textContent          = data.lr_prob + "%";
    document.getElementById("lrVerdict").textContent      = lrStatus;
    document.getElementById("lrVerdict").className        = "model-verdict-badge mvb-" + lrStatus;
    setBar("lrBar", data.lr_prob);
    populateReasons("lrReasons", data.lr_reasons || [], lrStatus);

    /* RF model */
    const rfStatus = classifyRisk(data.rf_prob);
    document.getElementById("rfPct").textContent          = data.rf_prob + "%";
    document.getElementById("rfVerdict").textContent      = rfStatus;
    document.getElementById("rfVerdict").className        = "model-verdict-badge mvb-" + rfStatus;
    setBar("rfBar", data.rf_prob);
    populateReasons("rfReasons", data.rf_reasons || [], rfStatus);
  }

  /* --- Reasons --- */
  const list = document.getElementById("reasonsList");
  list.innerHTML = "";
  (data.reasons || []).forEach(r => {
    const li = document.createElement("li");
    li.textContent = r;
    list.appendChild(li);
  });

  panel.classList.remove("hidden");
  panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/* Allow pressing Enter in the input */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("urlInput").addEventListener("keydown", event => {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) analyzeUrl();
  });
  loadModelMetrics();
});
