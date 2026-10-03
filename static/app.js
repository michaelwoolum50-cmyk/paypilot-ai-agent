async function post(url, body) {
  const r = await fetch(url, {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)});
  return r.json();
}
function showTrace(lines){ document.getElementById("trace").textContent = lines.join("\n"); }
function showResult(d){
  const el = document.getElementById("result");
  if (d.error) { el.innerHTML = `<p class="err">${d.error}</p>`; return; }
  if (d.status === "no_results") { el.innerHTML = `<p class="err">No listings matched. Try another product.</p>`; return; }
  if (d.status === "no_deal" || d.status === "watching") {
    el.innerHTML = `<p>No deal under budget right now. The agent keeps watching.</p>`; return;
  }
  const p = d.pick;
  let html = `<div class="pick"><h3>🏆 ${p.title}</h3>
    <div>$${p.price.toFixed(2)} · ${p.condition} · seller ${p.seller_rating}/5 · ships in ${p.shipping_days}d</div>
    <div>Agent score: ${d.score}/100</div>`;
  if (d.order_id) html += `<div>PayPal order: <code>${d.order_id}</code></div>
    <a class="approve" href="${d.approval_url}" target="_blank">Approve in PayPal sandbox →</a>`;
  else html += `<div><em>Preview mode — flip off "Preview only" to create a real PayPal sandbox order.</em></div>`;
  html += `</div>`;
  el.innerHTML = html;
}
document.getElementById("go").onclick = async (e) => {
  const btn = e.target; btn.disabled = true; btn.textContent = "Agent shopping…";
  showTrace(["Agent thinking…"]); document.getElementById("result").innerHTML = "";
  const d = await post("/api/shop", {
    query: document.getElementById("query").value,
    max_budget: document.getElementById("budget").value,
    dry_run: document.getElementById("dryrun").checked });
  showTrace(d.trace || [d.error || "error"]); showResult(d);
  btn.disabled = false; btn.textContent = "Let the agent shop 🛒";
};
document.getElementById("wgo").onclick = async (e) => {
  const btn = e.target; btn.disabled = true; btn.textContent = "Watching…";
  showTrace(["Agent watching prices…"]); document.getElementById("result").innerHTML = "";
  const d = await post("/api/watch", {
    query: document.getElementById("wquery").value,
    target_price: document.getElementById("wtarget").value,
    max_budget: document.getElementById("wcap").value });
  showTrace(d.trace || [d.error || "error"]); showResult(d);
  btn.disabled = false; btn.textContent = "Start watch 👀";
};
