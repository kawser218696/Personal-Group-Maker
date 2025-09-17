const API_PREFIX = "/api";
const storageKey = "tg_userbot_api_key";

function getApiKey() {
  return localStorage.getItem(storageKey);
}

function setApiKey(k) {
  localStorage.setItem(storageKey, k);
}

async function apiRequest(path, opts = {}) {
  const key = getApiKey();
  if (!opts.headers) opts.headers = {};
  if (key) {
    opts.headers["X-API-KEY"] = key;
  }
  if (!opts.headers["Content-Type"] && opts.body) {
    opts.headers["Content-Type"] = "application/json";
  }
  const res = await fetch(path, opts);
  const txt = await res.text();
  try {
    return { ok: res.ok, status: res.status, json: JSON.parse(txt) };
  } catch {
    return { ok: res.ok, status: res.status, text: txt };
  }
}

async function refreshSessions() {
  const el = document.getElementById("sessionsList");
  const sel = document.getElementById("sessionSelect");
  const bulk = document.getElementById("bulkSession");
  el.innerHTML = "";
  sel.innerHTML = "";
  bulk.innerHTML = "";
  const r = await apiRequest(API_PREFIX + "/sessions");
  if (!r.ok) {
    el.innerHTML = `<li style="color:red">Error: ${r.status} - ${JSON.stringify(r.json || r.text)}</li>`;
    return;
  }
  for (const name of r.json.sessions) {
    const li = document.createElement("li");
    li.textContent = name + " ";
    const del = document.createElement("button");
    del.textContent = "Delete";
    del.onclick = async () => {
      await apiRequest(API_PREFIX + `/sessions/${encodeURIComponent(name)}`, { method: "DELETE" });
      refreshSessions();
    };
    li.appendChild(del);
    el.appendChild(li);

    const opt = document.createElement("option"); opt.value = name; opt.textContent = name;
    sel.appendChild(opt.cloneNode(true));
    bulk.appendChild(opt);
  }
}

document.getElementById("saveKey").onclick = () => {
  const k = document.getElementById("apiKey").value.trim();
  setApiKey(k);
  refreshSessions();
};

document.getElementById("addSession").onclick = async () => {
  const name = document.getElementById("sessionName").value.trim();
  const ss = document.getElementById("sessionString").value.trim();
  if (!name || !ss) return alert("Provide name and string session.");
  const r = await apiRequest(API_PREFIX + "/sessions", { method: "POST", body: JSON.stringify({ name, string_session: ss }) });
  if (!r.ok) alert("Error: " + JSON.stringify(r.json || r.text));
  else {
    document.getElementById("sessionName").value = "";
    document.getElementById("sessionString").value = "";
    refreshSessions();
  }
};

document.getElementById("createGroup").onclick = async () => {
  const session = document.getElementById("sessionSelect").value;
  const title = document.getElementById("groupTitle").value.trim();
  const about = document.getElementById("groupAbout").value.trim();
  if (!session || !title) return alert("Select session and enter title.");
  const r = await apiRequest(API_PREFIX + "/create_supergroup", { method: "POST", body: JSON.stringify({ session_name: session, title, about }) });
  document.getElementById("createResult").textContent = JSON.stringify(r.json || r.text, null, 2);
  refreshSessions();
};

document.getElementById("bulkCreate").onclick = async () => {
  const session = document.getElementById("bulkSession").value;
  const titles = document.getElementById("bulkTitles").value.split("\n").map(s => s.trim()).filter(Boolean);
  if (!session || titles.length === 0) return alert("Select session and add titles.");
  const results = [];
  for (const t of titles) {
    const r = await apiRequest(API_PREFIX + "/create_supergroup", { method: "POST", body: JSON.stringify({ session_name: session, title: t }) });
    results.push({ title: t, result: r.json || r.text, ok: r.ok, status: r.status });
  }
  document.getElementById("bulkResult").textContent = JSON.stringify(results, null, 2);
  refreshSessions();
};

window.addEventListener("load", () => {
  const key = getApiKey();
  if (key) document.getElementById("apiKey").value = key;
  refreshSessions();
});