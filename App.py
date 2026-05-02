<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HIDDEN HOSTING — Underground Server Panel</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #020508;
    --surface: #050d12;
    --panel: #071018;
    --border: #0a2030;
    --accent: #00ffe1;
    --accent2: #00a8ff;
    --danger: #ff3e3e;
    --warn: #ffaa00;
    --green: #00ff88;
    --text: #c8dde8;
    --muted: #3a6070;
    --glow: 0 0 12px #00ffe166;
    --glow2: 0 0 20px #00a8ff44;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* GRID BG */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,255,225,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,255,225,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* SCAN LINE */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px);
    pointer-events: none;
    z-index: 0;
  }

  .wrap { position: relative; z-index: 1; max-width: 1200px; margin: 0 auto; padding: 0 24px 80px; }

  /* ===== HEADER ===== */
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 28px 0 20px;
    border-bottom: 1px solid var(--border);
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .logo-icon {
    width: 44px; height: 44px;
    border: 2px solid var(--accent);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    box-shadow: var(--glow), inset 0 0 10px #00ffe122;
    animation: pulse 3s ease-in-out infinite;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  }

  @keyframes pulse {
    0%, 100% { box-shadow: var(--glow), inset 0 0 10px #00ffe122; }
    50% { box-shadow: 0 0 25px #00ffe199, inset 0 0 18px #00ffe133; }
  }

  .logo-text h1 {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 900;
    letter-spacing: 4px;
    color: var(--accent);
    text-shadow: var(--glow);
  }

  .logo-text span {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 3px;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .status-pill {
    display: flex; align-items: center; gap: 7px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--green);
    border: 1px solid #00ff8844;
    padding: 5px 14px;
    letter-spacing: 1px;
  }

  .status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: blink 1.5s step-end infinite;
  }

  @keyframes blink { 50% { opacity: 0.2; } }

  .btn {
    font-family: 'Orbitron', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 9px 20px;
    border: 1px solid var(--accent);
    background: transparent;
    color: var(--accent);
    cursor: pointer;
    text-transform: uppercase;
    transition: all 0.2s;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
  }

  .btn:hover {
    background: var(--accent);
    color: #000;
    box-shadow: var(--glow);
  }

  .btn-danger {
    border-color: var(--danger);
    color: var(--danger);
  }
  .btn-danger:hover {
    background: var(--danger);
    color: #fff;
    box-shadow: 0 0 15px #ff3e3e88;
  }

  /* ===== HERO BANNER ===== */
  .hero {
    text-align: center;
    padding: 60px 0 50px;
    position: relative;
  }

  .hero-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 5px;
    color: var(--muted);
    margin-bottom: 16px;
  }

  .hero h2 {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2rem, 5vw, 3.8rem);
    font-weight: 900;
    color: #fff;
    line-height: 1.1;
    letter-spacing: 2px;
    margin-bottom: 10px;
  }

  .hero h2 span {
    color: var(--accent);
    text-shadow: var(--glow);
  }

  .hero-sub {
    font-size: 1.1rem;
    color: var(--muted);
    letter-spacing: 1px;
    margin-bottom: 36px;
  }

  /* ===== PLAN CARDS ===== */
  .section-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 4px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 12px;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border), transparent);
  }

  .plan-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 50px;
  }

  .plan-card {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.2s;
    clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 20px 100%, 0 100%);
  }

  .plan-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, var(--accent), transparent);
    opacity: 0;
    transition: opacity 0.3s;
  }

  .plan-card:hover {
    border-color: var(--accent);
    transform: translateY(-4px);
  }
  .plan-card:hover::before { opacity: 1; }

  .plan-card.featured {
    border-color: var(--accent);
    background: linear-gradient(135deg, #071018, #0a1f2f);
  }
  .plan-card.featured::before { opacity: 1; }

  .featured-badge {
    position: absolute;
    top: 16px; right: -8px;
    font-family: 'Orbitron', monospace;
    font-size: 0.55rem;
    letter-spacing: 2px;
    background: var(--accent);
    color: #000;
    padding: 4px 20px 4px 10px;
    font-weight: 700;
    clip-path: polygon(0 0, 100% 0, 90% 100%, 0 100%);
  }

  .plan-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: var(--muted);
    margin-bottom: 8px;
  }

  .plan-price {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    color: var(--accent);
    text-shadow: var(--glow);
    line-height: 1;
    margin-bottom: 4px;
  }

  .plan-price span {
    font-size: 0.9rem;
    color: var(--muted);
  }

  .plan-desc {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 22px;
    letter-spacing: 0.5px;
  }

  .plan-specs {
    list-style: none;
    margin-bottom: 26px;
  }

  .plan-specs li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  .plan-specs li:last-child { border-bottom: none; }

  .spec-icon {
    font-size: 1rem;
    width: 22px;
    text-align: center;
  }

  .spec-label { color: var(--muted); font-size: 0.75rem; margin-left: auto; font-family: 'Share Tech Mono', monospace; }

  /* ===== RESOURCE MONITOR ===== */
  .monitor-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 50px;
  }

  @media (max-width: 640px) { .monitor-grid { grid-template-columns: 1fr; } }

  .monitor-card {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 22px;
    position: relative;
  }

  .monitor-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 12px;
  }

  .monitor-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 14px;
    line-height: 1;
  }

  .monitor-bar-wrap {
    height: 6px;
    background: #0a2030;
    position: relative;
    overflow: hidden;
  }

  .monitor-bar {
    height: 100%;
    position: relative;
    animation: barLoad 1.5s ease-out forwards;
    transform-origin: left;
  }

  .monitor-bar::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0;
    width: 20px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.4));
  }

  @keyframes barLoad {
    from { width: 0% !important; }
  }

  .bar-ram { background: linear-gradient(to right, #00a8ff, #00ffe1); width: 42%; }
  .bar-disk { background: linear-gradient(to right, #7c3aed, #a855f7); width: 58%; }
  .bar-cpu { background: linear-gradient(to right, #ff6b00, #ffaa00); width: 28%; }

  .val-ram { color: var(--accent2); text-shadow: 0 0 12px #00a8ff88; }
  .val-disk { color: #a855f7; text-shadow: 0 0 12px #a855f788; }
  .val-cpu { color: var(--warn); text-shadow: 0 0 12px #ffaa0088; }

  .monitor-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    color: var(--muted);
    margin-top: 8px;
  }

  /* ===== LIMITS TABLE ===== */
  .limits-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    margin-bottom: 50px;
    overflow: hidden;
  }

  .limits-header {
    background: linear-gradient(to right, #0a1f2f, var(--panel));
    padding: 18px 24px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 12px;
  }

  .limits-header h3 {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: var(--accent);
  }

  .limits-table { width: 100%; border-collapse: collapse; }

  .limits-table th {
    text-align: left;
    padding: 12px 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    text-transform: uppercase;
  }

  .limits-table td {
    padding: 14px 24px;
    border-bottom: 1px solid #0a2030;
    font-size: 0.9rem;
    font-weight: 600;
  }

  .limits-table tr:last-child td { border-bottom: none; }

  .limits-table tr:hover td { background: #071825; }

  .limit-badge {
    display: inline-block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border: 1px solid;
    letter-spacing: 1px;
  }

  .badge-cyan { border-color: var(--accent); color: var(--accent); }
  .badge-blue { border-color: var(--accent2); color: var(--accent2); }
  .badge-warn { border-color: var(--warn); color: var(--warn); }
  .badge-danger { border-color: var(--danger); color: var(--danger); }
  .badge-green { border-color: var(--green); color: var(--green); }
  .badge-purple { border-color: #a855f7; color: #a855f7; }

  /* ===== KILL METHOD ===== */
  .kill-panel {
    background: linear-gradient(135deg, #0d0505, #150a0a);
    border: 1px solid #3a1010;
    margin-bottom: 50px;
    overflow: hidden;
    position: relative;
  }

  .kill-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, var(--danger), transparent);
  }

  .kill-header {
    padding: 18px 24px;
    border-bottom: 1px solid #3a1010;
    display: flex; align-items: center; gap: 12px;
  }

  .kill-header h3 {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: var(--danger);
    text-shadow: 0 0 10px #ff3e3e66;
  }

  .kill-body { padding: 28px; }

  .kill-steps {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }

  .kill-step {
    background: #0a0505;
    border: 1px solid #2a0808;
    padding: 18px;
    position: relative;
  }

  .kill-step-num {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 900;
    color: #2a0808;
    position: absolute;
    top: 10px; right: 14px;
  }

  .kill-step-icon { font-size: 1.4rem; margin-bottom: 8px; }

  .kill-step h4 {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: var(--danger);
    margin-bottom: 6px;
  }

  .kill-step p {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    line-height: 1.5;
  }

  .kill-code {
    background: #080303;
    border: 1px solid #2a0808;
    padding: 18px 22px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: #ff7070;
    line-height: 1.8;
    overflow-x: auto;
  }

  .kill-code .comment { color: #4a1515; }
  .kill-code .cmd { color: var(--danger); }
  .kill-code .var { color: var(--warn); }
  .kill-code .val { color: var(--accent); }

  /* ===== SIGN UP FORM ===== */
  .signup-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 40px;
    max-width: 560px;
    margin: 0 auto 50px;
    position: relative;
    clip-path: polygon(0 0, calc(100% - 30px) 0, 100% 30px, 100% 100%, 30px 100%, 0 100%);
  }

  .signup-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(to right, var(--accent), var(--accent2));
  }

  .form-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    letter-spacing: 3px;
    color: var(--accent);
    text-align: center;
    margin-bottom: 28px;
    text-shadow: var(--glow);
  }

  .form-group { margin-bottom: 18px; }

  .form-group label {
    display: block;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--muted);
    margin-bottom: 7px;
    text-transform: uppercase;
  }

  .form-control {
    width: 100%;
    background: #020a10;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 12px 16px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    outline: none;
    transition: border-color 0.2s;
  }

  .form-control:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px #00ffe111;
  }

  .form-control::placeholder { color: var(--muted); }

  .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

  .btn-full {
    width: 100%;
    padding: 14px;
    font-size: 0.8rem;
    clip-path: polygon(12px 0%, 100% 0%, calc(100% - 12px) 100%, 0% 100%);
  }

  /* ===== FOOTER ===== */
  footer {
    border-top: 1px solid var(--border);
    padding: 30px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 14px;
  }

  .footer-brand {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: var(--muted);
  }

  .footer-links {
    display: flex; gap: 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
  }

  .footer-links a {
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s;
  }
  .footer-links a:hover { color: var(--accent); }

  /* ===== TICKER ===== */
  .ticker-wrap {
    overflow: hidden;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 9px 0;
    margin: 30px 0;
    background: #030c12;
  }

  .ticker {
    display: flex;
    white-space: nowrap;
    animation: ticker 25s linear infinite;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 2px;
    gap: 60px;
  }

  @keyframes ticker {
    from { transform: translateX(0); }
    to { transform: translateX(-50%); }
  }

  .ticker span { color: var(--accent); }

  /* NODE STATS */
  .node-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 50px;
  }

  .node-card {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .node-card::before {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
    transform: scaleX(0);
    transition: transform 0.3s;
  }

  .node-card:hover::before { transform: scaleX(1); }

  .node-val {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
    text-shadow: var(--glow);
    line-height: 1;
    margin-bottom: 6px;
  }

  .node-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  select.form-control {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2300ffe1'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 14px center;
  }
</style>
</head>
<body>

<div class="wrap">

  <!-- HEADER -->
  <header>
    <div class="logo">
      <div class="logo-icon">⬡</div>
      <div class="logo-text">
        <h1>HIDDEN HOSTING</h1>
        <span>// UNDERGROUND INFRASTRUCTURE</span>
      </div>
    </div>
    <div class="header-right">
      <div class="status-pill">
        <div class="status-dot"></div>
        ALL NODES ONLINE
      </div>
      <button class="btn">DEPLOY NOW</button>
    </div>
  </header>

  <!-- TICKER -->
  <div class="ticker-wrap">
    <div class="ticker">
      <span>⬡</span> NODE-01 ONLINE &nbsp;|&nbsp; <span>⬡</span> NODE-02 ONLINE &nbsp;|&nbsp; <span>⬡</span> NODE-03 ONLINE &nbsp;|&nbsp;
      RAM LIMIT: <span>100MB / USER</span> &nbsp;|&nbsp; DISK LIMIT: <span>250MB / USER</span> &nbsp;|&nbsp; CPU LIMIT: <span>15% / USER</span> &nbsp;|&nbsp;
      KILL METHOD: <span>ACTIVE</span> &nbsp;|&nbsp; NO DOCKER REQUIRED &nbsp;|&nbsp; UPTIME: <span>99.7%</span> &nbsp;|&nbsp;
      <span>⬡</span> NODE-01 ONLINE &nbsp;|&nbsp; <span>⬡</span> NODE-02 ONLINE &nbsp;|&nbsp; <span>⬡</span> NODE-03 ONLINE &nbsp;|&nbsp;
      RAM LIMIT: <span>100MB / USER</span> &nbsp;|&nbsp; DISK LIMIT: <span>250MB / USER</span> &nbsp;|&nbsp; CPU LIMIT: <span>15% / USER</span> &nbsp;|&nbsp;
      KILL METHOD: <span>ACTIVE</span> &nbsp;|&nbsp; NO DOCKER REQUIRED &nbsp;|&nbsp; UPTIME: <span>99.7%</span> &nbsp;|&nbsp;
    </div>
  </div>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-label">// FREE &amp; ANONYMOUS CLOUD HOSTING</div>
    <h2>STAY <span>HIDDEN</span>,<br>STAY ONLINE</h2>
    <p class="hero-sub">No Docker. No bloat. Pure process isolation with kill enforcement.</p>
    <button class="btn" style="font-size:0.8rem; padding:14px 36px; clip-path:polygon(10px 0%,100% 0%,calc(100% - 10px) 100%,0% 100%)">
      ⬡ START FOR FREE
    </button>
  </div>

  <!-- NODE STATS -->
  <div class="section-title">// INFRASTRUCTURE STATUS</div>
  <div class="node-grid">
    <div class="node-card"><div class="node-val">3</div><div class="node-lbl">Active Nodes</div></div>
    <div class="node-card"><div class="node-val">99.7%</div><div class="node-lbl">Uptime</div></div>
    <div class="node-card"><div class="node-val">100<span style="font-size:1rem">MB</span></div><div class="node-lbl">RAM / User</div></div>
    <div class="node-card"><div class="node-val">250<span style="font-size:1rem">MB</span></div><div class="node-lbl">Disk / User</div></div>
    <div class="node-card"><div class="node-val">15<span style="font-size:1rem">%</span></div><div class="node-lbl">CPU / User</div></div>
    <div class="node-card"><div class="node-val">∞</div><div class="node-lbl">Bandwidth</div></div>
    <div class="node-card"><div class="node-val">0</div><div class="node-lbl">Docker Deps</div></div>
    <div class="node-card"><div class="node-val">KILL</div><div class="node-lbl">Enforce Method</div></div>
  </div>

  <!-- RESOURCE MONITOR -->
  <div class="section-title">// PER-USER RESOURCE LIMITS</div>
  <div class="monitor-grid">
    <div class="monitor-card">
      <div class="monitor-label">// RAM LIMIT</div>
      <div class="monitor-value val-ram">100 <span style="font-size:1rem;color:var(--muted)">MB</span></div>
      <div class="monitor-bar-wrap">
        <div class="monitor-bar bar-ram"></div>
      </div>
      <div class="monitor-sub">42MB avg usage · Hard limit enforced</div>
    </div>
    <div class="monitor-card">
      <div class="monitor-label">// DISK LIMIT</div>
      <div class="monitor-value val-disk">250 <span style="font-size:1rem;color:var(--muted)">MB</span></div>
      <div class="monitor-bar-wrap">
        <div class="monitor-bar bar-disk"></div>
      </div>
      <div class="monitor-sub">145MB avg usage · quota enforced</div>
    </div>
    <div class="monitor-card">
      <div class="monitor-label">// CPU LIMIT</div>
      <div class="monitor-value val-cpu">15 <span style="font-size:1rem;color:var(--muted)">%</span></div>
      <div class="monitor-bar-wrap">
        <div class="monitor-bar bar-cpu"></div>
      </div>
      <div class="monitor-sub">4.2% avg usage · Kill on exceed</div>
    </div>
  </div>

  <!-- LIMITS TABLE -->
  <div class="section-title">// PLAN SPECIFICATIONS</div>
  <div class="limits-panel">
    <div class="limits-header">
      <span style="color:var(--accent);font-size:1.1rem">⬡</span>
      <h3>RESOURCE ALLOCATION TABLE</h3>
    </div>
    <table class="limits-table">
      <thead>
        <tr>
          <th>RESOURCE</th>
          <th>LIMIT</th>
          <th>ENFORCEMENT</th>
          <th>ACTION ON EXCEED</th>
          <th>STATUS</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>🧠 RAM Memory</td>
          <td><span class="limit-badge badge-cyan">100 MB</span></td>
          <td>cgroup v2 memory.max</td>
          <td><span class="limit-badge badge-danger">PROCESS KILL</span></td>
          <td><span class="limit-badge badge-green">ACTIVE</span></td>
        </tr>
        <tr>
          <td>💾 Disk Storage</td>
          <td><span class="limit-badge badge-purple">250 MB</span></td>
          <td>Linux disk quota</td>
          <td><span class="limit-badge badge-warn">WRITE BLOCKED</span></td>
          <td><span class="limit-badge badge-green">ACTIVE</span></td>
        </tr>
        <tr>
          <td>⚙️ CPU Usage</td>
          <td><span class="limit-badge badge-warn">15%</span></td>
          <td>cgroup cpu.max</td>
          <td><span class="limit-badge badge-danger">PROCESS KILL</span></td>
          <td><span class="limit-badge badge-green">ACTIVE</span></td>
        </tr>
        <tr>
          <td>🌐 Network I/O</td>
          <td><span class="limit-badge badge-blue">Unlimited</span></td>
          <td>—</td>
          <td>—</td>
          <td><span class="limit-badge badge-green">OPEN</span></td>
        </tr>
        <tr>
          <td>🐳 Docker Engine</td>
          <td><span class="limit-badge badge-danger">DISABLED</span></td>
          <td>kernel namespaces</td>
          <td>—</td>
          <td><span class="limit-badge badge-warn">NOT USED</span></td>
        </tr>
        <tr>
          <td>📡 Uptime Monitor</td>
          <td><span class="limit-badge badge-cyan">24/7</span></td>
          <td>auto-restart</td>
          <td>—</td>
          <td><span class="limit-badge badge-green">RUNNING</span></td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- KILL METHOD -->
  <div class="section-title">// KILL METHOD — ENFORCEMENT ENGINE</div>
  <div class="kill-panel">
    <div class="kill-header">
      <span style="color:var(--danger);font-size:1.1rem">☠</span>
      <h3>PROCESS KILL ENFORCEMENT — NO DOCKER REQUIRED</h3>
    </div>
    <div class="kill-body">
      <div class="kill-steps">
        <div class="kill-step">
          <div class="kill-step-num">01</div>
          <div class="kill-step-icon">📊</div>
          <h4>MONITOR</h4>
          <p>cgroup v2 tracks RAM &amp; CPU per user PID in real-time every 500ms</p>
        </div>
        <div class="kill-step">
          <div class="kill-step-num">02</div>
          <div class="kill-step-icon">⚠️</div>
          <h4>DETECT</h4>
          <p>Threshold breach detected → RAM &gt; 100MB or CPU &gt; 15% sustained</p>
        </div>
        <div class="kill-step">
          <div class="kill-step-num">03</div>
          <div class="kill-step-icon">☠</div>
          <h4>KILL</h4>
          <p>SIGKILL sent to entire process group — instant termination, no grace</p>
        </div>
        <div class="kill-step">
          <div class="kill-step-num">04</div>
          <div class="kill-step-icon">📝</div>
          <h4>LOG</h4>
          <p>Kill event logged with PID, user, resource, timestamp to audit trail</p>
        </div>
      </div>

      <div class="kill-code">
<span class="comment"># HIDDEN HOSTING — Kill Method (no Docker)</span><br>
<span class="comment"># cgroup v2 per-user enforcement script</span><br><br>
<span class="cmd">USER_CGROUP</span>=<span class="val">"/sys/fs/cgroup/user_$USER_ID"</span><br><br>
<span class="comment"># Set RAM hard limit: 100MB</span><br>
<span class="cmd">echo</span> <span class="val">"104857600"</span> &gt; <span class="var">$USER_CGROUP</span>/memory.max<br><br>
<span class="comment"># Set CPU limit: 15% (15000us per 100000us period)</span><br>
<span class="cmd">echo</span> <span class="val">"15000 100000"</span> &gt; <span class="var">$USER_CGROUP</span>/cpu.max<br><br>
<span class="comment"># Set disk quota: 250MB (512 blocks of 512B)</span><br>
<span class="cmd">setquota</span> -u <span class="var">$USER_ID</span> <span class="val">256000 256000 0 0</span> /dev/sda1<br><br>
<span class="comment"># Kill on OOM (memory.oom.group = 1)</span><br>
<span class="cmd">echo</span> <span class="val">"1"</span> &gt; <span class="var">$USER_CGROUP</span>/memory.oom.group<br><br>
<span class="comment"># Monitor loop — SIGKILL if CPU threshold exceeded</span><br>
<span class="cmd">while</span> true; do<br>
&nbsp;&nbsp;CPU_USAGE=$(<span class="cmd">cat</span> <span class="var">$USER_CGROUP</span>/cpu.stat | <span class="cmd">grep</span> usage_usec)<br>
&nbsp;&nbsp;<span class="cmd">if</span> [[ $CPU_USAGE &gt; $CPU_LIMIT ]]; then<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="cmd">kill</span> <span class="val">-9 -$(cat $USER_CGROUP/cgroup.procs)</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="cmd">logger</span> <span class="val">"[HIDDEN] KILLED user_$USER_ID — CPU exceeded 15%"</span><br>
&nbsp;&nbsp;<span class="cmd">fi</span><br>
&nbsp;&nbsp;<span class="cmd">sleep</span> <span class="val">0.5</span><br>
<span class="cmd">done</span>
      </div>
    </div>
  </div>

  <!-- PLANS -->
  <div class="section-title">// HOSTING PLANS</div>
  <div class="plan-grid">
    <div class="plan-card">
      <div class="plan-name">// GHOST</div>
      <div class="plan-price">FREE<span>/mo</span></div>
      <div class="plan-desc">Anonymous. No card. No questions.</div>
      <ul class="plan-specs">
        <li><span class="spec-icon">🧠</span> RAM <span class="spec-label">100 MB</span></li>
        <li><span class="spec-icon">💾</span> Disk <span class="spec-label">250 MB</span></li>
        <li><span class="spec-icon">⚙️</span> CPU <span class="spec-label">15%</span></li>
        <li><span class="spec-icon">🌐</span> Bandwidth <span class="spec-label">Unlimited</span></li>
        <li><span class="spec-icon">☠</span> Kill Method <span class="spec-label">Enabled</span></li>
        <li><span class="spec-icon">🐳</span> Docker <span class="spec-label">Not Needed</span></li>
      </ul>
      <button class="btn btn-full">DEPLOY FREE</button>
    </div>

    <div class="plan-card featured">
      <div class="featured-badge">POPULAR</div>
      <div class="plan-name">// PHANTOM</div>
      <div class="plan-price">$2<span>/mo</span></div>
      <div class="plan-desc">More power. Same privacy. Same kill.</div>
      <ul class="plan-specs">
        <li><span class="spec-icon">🧠</span> RAM <span class="spec-label">512 MB</span></li>
        <li><span class="spec-icon">💾</span> Disk <span class="spec-label">2 GB</span></li>
        <li><span class="spec-icon">⚙️</span> CPU <span class="spec-label">50%</span></li>
        <li><span class="spec-icon">🌐</span> Bandwidth <span class="spec-label">Unlimited</span></li>
        <li><span class="spec-icon">☠</span> Kill Method <span class="spec-label">Enabled</span></li>
        <li><span class="spec-icon">🔒</span> Priority Support <span class="spec-label">✓</span></li>
      </ul>
      <button class="btn btn-full">DEPLOY PHANTOM</button>
    </div>

    <div class="plan-card">
      <div class="plan-name">// SPECTER</div>
      <div class="plan-price">$5<span>/mo</span></div>
      <div class="plan-desc">Full power. Full anonymity. Full kill.</div>
      <ul class="plan-specs">
        <li><span class="spec-icon">🧠</span> RAM <span class="spec-label">2 GB</span></li>
        <li><span class="spec-icon">💾</span> Disk <span class="spec-label">10 GB</span></li>
        <li><span class="spec-icon">⚙️</span> CPU <span class="spec-label">100%</span></li>
        <li><span class="spec-icon">🌐</span> Bandwidth <span class="spec-label">Unlimited</span></li>
        <li><span class="spec-icon">☠</span> Kill Method <span class="spec-label">Custom</span></li>
        <li><span class="spec-icon">⚡</span> Dedicated Node <span class="spec-label">✓</span></li>
      </ul>
      <button class="btn btn-full">DEPLOY SPECTER</button>
    </div>
  </div>

  <!-- SIGNUP -->
  <div class="section-title">// DEPLOY YOUR APP</div>
  <div class="signup-panel">
    <div class="form-title">⬡ CREATE DEPLOYMENT</div>
    <div class="form-row">
      <div class="form-group">
        <label>// Username</label>
        <input class="form-control" type="text" placeholder="ghost_user">
      </div>
      <div class="form-group">
        <label>// App Name</label>
        <input class="form-control" type="text" placeholder="my-bot">
      </div>
    </div>
    <div class="form-group">
      <label>// Email (optional)</label>
      <input class="form-control" type="email" placeholder="stay@anonymous.net">
    </div>
    <div class="form-group">
      <label>// Runtime</label>
      <select class="form-control">
        <option>Python 3.11</option>
        <option>Node.js 20</option>
        <option>Bash Script</option>
        <option>Go 1.22</option>
      </select>
    </div>
    <div class="form-group">
      <label>// Start Command</label>
      <input class="form-control" type="text" placeholder="python3 bot.py">
    </div>
    <div class="form-group">
      <label>// Plan</label>
      <select class="form-control">
        <option>GHOST — Free (100MB RAM / 250MB Disk / 15% CPU)</option>
        <option>PHANTOM — $2/mo (512MB / 2GB / 50%)</option>
        <option>SPECTER — $5/mo (2GB / 10GB / 100%)</option>
      </select>
    </div>
    <button class="btn btn-full" style="margin-top:8px">⬡ DEPLOY NOW — INSTANT START</button>
  </div>

  <!-- FOOTER -->
  <footer>
    <div class="footer-brand">⬡ HIDDEN HOSTING — v2.4.1</div>
    <div class="footer-links">
      <a href="#">DOCS</a>
      <a href="#">API</a>
      <a href="#">STATUS</a>
      <a href="#">TERMS</a>
      <a href="#">CONTACT</a>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;color:var(--muted)">
      NO DOCKER · KILL METHOD · 99.7% UPTIME
    </div>
  </footer>

</div>

<script>
  // Animate monitor bars on scroll
  const bars = document.querySelectorAll('.monitor-bar');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if(e.isIntersecting) {
        e.target.style.animationPlayState = 'running';
      }
    });
  }, { threshold: 0.3 });
  bars.forEach(b => {
    b.style.animationPlayState = 'paused';
    observer.observe(b);
  });

  // Hover flicker effect on logo icon
  const logoIcon = document.querySelector('.logo-icon');
  setInterval(() => {
    if(Math.random() > 0.96) {
      logoIcon.style.opacity = '0.4';
      setTimeout(() => logoIcon.style.opacity = '1', 60);
    }
  }, 200);

  // Live "node" counter animation
  const nodeVals = document.querySelectorAll('.node-val');
  nodeVals.forEach(el => {
    el.style.transition = 'text-shadow 0.3s';
    el.addEventListener('mouseenter', () => {
      el.style.textShadow = '0 0 30px #00ffe1';
    });
    el.addEventListener('mouseleave', () => {
      el.style.textShadow = '';
    });
  });
</script>
</body>
</html>
