<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Shipment Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f5f7fb; color: #111827; }
        header { background: #0f766e; color: #fff; padding: 1rem 1.5rem; }
        main { padding: 1rem 1.5rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        .card { background: #fff; border-radius: 10px; padding: 1rem; box-shadow: 0 1px 8px rgba(0,0,0,0.08); }
        h2 { margin-top: 0; }
        ul { padding-left: 1rem; }
        label { display: block; margin-top: .5rem; font-weight: 600; }
        input, select, button { width: 100%; padding: .5rem; margin-top: .25rem; }
        button { background: #0f766e; color: #fff; border: 0; border-radius: 6px; cursor: pointer; margin-top: .75rem; }
        .status { font-size: .9rem; margin-top: .5rem; min-height: 1.2rem; }
        @media (max-width: 900px) { main { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
<header>
    <h1>Shipment Dashboard</h1>
    <p>Quick visual view of Ports and Vessels API data.</p>
</header>
<main>
    <section class="card">
        <h2>Ports</h2>
        <ul id="ports-list"></ul>

        <h3>Add Port</h3>
        <form id="port-form">
            <label>UN/LOCODE <input name="unlocode" required></label>
            <label>Name <input name="name" required></label>
            <label>Country Code <input name="countryCode" maxlength="2" required></label>
            <label>Timezone <input name="timezone" value="UTC"></label>
            <button type="submit">Create Port</button>
            <div class="status" id="port-status"></div>
        </form>
    </section>

    <section class="card">
        <h2>Vessels</h2>
        <ul id="vessels-list"></ul>

        <h3>Add Vessel</h3>
        <form id="vessel-form">
            <label>IMO Number <input name="imoNumber" required></label>
            <label>Name <input name="name" required></label>
            <label>Vessel Type <input name="vesselType" value="Container"></label>
            <label>Flag <input name="flag" maxlength="2" value="US"></label>
            <label>Destination Port
                <select name="destinationPortId" id="destination-port"></select>
            </label>
            <button type="submit">Create Vessel</button>
            <div class="status" id="vessel-status"></div>
        </form>
    </section>
</main>

<script>
async function api(path, opts = {}) {
    const res = await fetch(path, {
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        ...opts,
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text}`);
    }
    return res.status === 204 ? null : res.json();
}

function normalizeCollection(data) {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data.member)) return data.member;
    if (Array.isArray(data['hydra:member'])) return data['hydra:member'];
    return [];
}

function renderList(id, items, formatter) {
    document.getElementById(id).innerHTML = items.map(i => `<li>${formatter(i)}</li>`).join('') || '<li>No data yet</li>';
}

async function loadData() {
    const [portsRes, vesselsRes] = await Promise.all([
        api('/api/ports'),
        api('/api/vessels'),
    ]);

    const ports = normalizeCollection(portsRes);
    const vessels = normalizeCollection(vesselsRes);

    renderList('ports-list', ports, p => `${p.unlocode} - ${p.name} (${p.countryCode ?? p.country_code})`);
    renderList('vessels-list', vessels, v => `${v.imoNumber ?? v.imo_number} - ${v.name}`);

    const portSelect = document.getElementById('destination-port');
    portSelect.innerHTML = '<option value="">None</option>' +
        ports.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
}

function formToPayload(form) {
    const fd = new FormData(form);
    const payload = Object.fromEntries(fd.entries());
    Object.keys(payload).forEach(key => {
        if (payload[key] === '') payload[key] = null;
    });
    return payload;
}

document.getElementById('port-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = document.getElementById('port-status');
    try {
        await api('/api/ports', { method: 'POST', body: JSON.stringify(formToPayload(e.target)) });
        status.textContent = 'Port created.';
        e.target.reset();
        await loadData();
    } catch (err) {
        status.textContent = err.message;
    }
});

document.getElementById('vessel-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = document.getElementById('vessel-status');
    try {
        await api('/api/vessels', { method: 'POST', body: JSON.stringify(formToPayload(e.target)) });
        status.textContent = 'Vessel created.';
        e.target.reset();
        await loadData();
    } catch (err) {
        status.textContent = err.message;
    }
});

loadData().catch((err) => {
    document.getElementById('port-status').textContent = err.message;
    document.getElementById('vessel-status').textContent = err.message;
});
</script>
</body>
</html>
<?php /**PATH /app/resources/views/dashboard.blade.php ENDPATH**/ ?>