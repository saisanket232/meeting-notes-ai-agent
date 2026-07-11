import json

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from agents.meeting_agent import analyze_meeting


app = FastAPI(title="AI Meeting Notes Agent")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Meeting Notes Agent</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
    <style>
        :root {
            --bg: #0b0f14;
            --card: #121826;
            --accent: #4f8cff;
            --accent-2: #7dd3fc;
            --success: #34d399;
            --warning: #fbbf24;
            --text: #e5eefb;
            --muted: #a8b3c7;
            --border: #22304a;
        }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;
            background: radial-gradient(ellipse at top, #132036 0%, var(--bg) 55%);
            color: var(--text);
            min-height: 100vh;
        }
        .wrap {
            max-width: 960px;
            margin: 0 auto;
            padding: 52px 20px 80px;
        }

        /* ── Hero ── */
        .hero {
            text-align: center;
            margin-bottom: 40px;
        }
        .hero h1 {
            font-size: clamp(2rem, 5vw, 3.2rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
        }
        .hero p {
            color: var(--muted);
            max-width: 640px;
            margin: 0 auto;
            line-height: 1.65;
            font-size: 1.05rem;
        }

        /* ── Cards ── */
        .card {
            background: rgba(18, 24, 38, 0.85);
            border: 1px solid var(--border);
            border-radius: 20px;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
            padding: 28px 32px;
            backdrop-filter: blur(16px);
            margin-bottom: 24px;
        }
        .card h2 {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--accent-2);
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card h2 .icon {
            font-size: 1.3rem;
        }

        /* ── Upload zone ── */
        .upload-zone {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
            padding: 16px 0 4px;
        }
        .drop-area {
            width: 100%;
            max-width: 480px;
            border: 2px dashed var(--border);
            border-radius: 16px;
            padding: 28px 20px;
            text-align: center;
            color: var(--muted);
            cursor: pointer;
            transition: border-color 0.2s, background 0.2s;
            position: relative;
        }
        .drop-area:hover, .drop-area.dragover {
            border-color: var(--accent);
            background: rgba(79, 140, 255, 0.06);
        }
        .drop-area input[type="file"] {
            position: absolute;
            inset: 0;
            opacity: 0;
            cursor: pointer;
        }
        .drop-area .drop-icon { font-size: 2rem; margin-bottom: 8px; }
        .drop-area .drop-label { font-size: 0.95rem; }
        #file-name {
            font-size: 0.88rem;
            color: var(--accent-2);
            min-height: 18px;
        }
        .info-box {
            width: 100%;
            max-width: 480px;
            background: rgba(79, 140, 255, 0.08);
            border: 1px solid rgba(79, 140, 255, 0.25);
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 0.9rem;
            color: var(--muted);
        }
        .btn {
            border: none;
            border-radius: 999px;
            padding: 13px 32px;
            font-size: 1rem;
            font-weight: 700;
            font-family: inherit;
            color: #fff;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            cursor: pointer;
            transition: opacity 0.2s, transform 0.15s;
            box-shadow: 0 4px 20px rgba(79, 140, 255, 0.35);
        }
        .btn:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .status-msg {
            min-height: 22px;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--accent-2);
            text-align: center;
        }
        .status-msg.error { color: #f87171; }

        /* ── Divider ── */
        hr.divider {
            border: none;
            border-top: 1px solid var(--border);
            margin: 4px 0 20px;
        }

        /* ── Results sections ── */
        #results { display: none; }

        .summary-text {
            color: var(--text);
            line-height: 1.75;
            font-size: 1rem;
        }

        .decisions-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .decisions-list li {
            display: flex;
            gap: 10px;
            align-items: flex-start;
            padding: 10px 14px;
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            border-radius: 10px;
            font-size: 0.97rem;
            line-height: 1.5;
        }
        .decisions-list li::before {
            content: "✓";
            color: var(--success);
            font-weight: 700;
            flex-shrink: 0;
            margin-top: 1px;
        }

        /* ── Action items table ── */
        .table-wrap { overflow-x: auto; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.93rem;
        }
        thead tr {
            background: rgba(79, 140, 255, 0.12);
        }
        th {
            text-align: left;
            padding: 12px 16px;
            color: var(--accent-2);
            font-weight: 600;
            border-bottom: 1px solid var(--border);
        }
        td {
            padding: 11px 16px;
            border-bottom: 1px solid rgba(34, 48, 74, 0.6);
            color: var(--text);
            vertical-align: top;
        }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: rgba(255,255,255,0.02); }

        /* ── Download button ── */
        .download-row {
            display: flex;
            justify-content: flex-end;
            margin-top: 4px;
        }
        .btn-download {
            border: 1px solid var(--accent);
            border-radius: 999px;
            padding: 9px 22px;
            font-size: 0.9rem;
            font-weight: 600;
            font-family: inherit;
            color: var(--accent-2);
            background: transparent;
            cursor: pointer;
            transition: background 0.2s, color 0.2s;
            display: flex;
            align-items: center;
            gap: 7px;
        }
        .btn-download:hover {
            background: rgba(79, 140, 255, 0.12);
            color: #fff;
        }

        /* ── Spinner ── */
        .spinner {
            display: inline-block;
            width: 16px; height: 16px;
            border: 2px solid rgba(125,211,252,0.3);
            border-top-color: var(--accent-2);
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            vertical-align: middle;
            margin-right: 6px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* ── Success banner ── */
        .success-banner {
            background: rgba(52, 211, 153, 0.1);
            border: 1px solid rgba(52, 211, 153, 0.35);
            border-radius: 12px;
            padding: 12px 18px;
            color: var(--success);
            font-weight: 600;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 24px;
        }
    </style>
</head>
<body>
    <div class="wrap">
        <!-- Hero -->
        <div class="hero">
            <h1>📝 AI Meeting Notes Agent</h1>
            <p>Upload a meeting transcript and automatically generate a summary, key decisions, and action items — powered by Groq.</p>
        </div>

        <!-- Upload card -->
        <div class="card">
            <h2><span class="icon">📂</span> Upload Meeting Transcript</h2>
            <hr class="divider" />
            <div class="upload-zone">
                <div class="drop-area" id="drop-area">
                    <div class="drop-icon">📄</div>
                    <div class="drop-label">Drag & drop a <strong>.txt</strong> file here, or click to browse</div>
                    <input type="file" id="file" accept=".txt" />
                </div>
                <div id="file-name"></div>
                <div class="info-box">ℹ️ Upload a <code>.txt</code> meeting transcript to generate a summary, key decisions, action items, and a downloadable JSON report.</div>
                <button class="btn" id="analyze-btn" disabled>Analyze Meeting</button>
                <div class="status-msg" id="status"></div>
            </div>
        </div>

        <!-- Success banner (hidden until analysis complete) -->
        <div class="success-banner" id="success-banner" style="display:none;">
            ✅ Analysis Complete!
        </div>

        <!-- Results -->
        <div id="results">
            <!-- Summary -->
            <div class="card">
                <h2><span class="icon">📝</span> Meeting Summary</h2>
                <hr class="divider" />
                <p class="summary-text" id="summary"></p>
            </div>

            <!-- Key Decisions -->
            <div class="card">
                <h2><span class="icon">✅</span> Key Decisions</h2>
                <hr class="divider" />
                <ul class="decisions-list" id="decisions"></ul>
            </div>

            <!-- Action Items -->
            <div class="card">
                <h2><span class="icon">📋</span> Action Items</h2>
                <hr class="divider" />
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr id="action-header"></tr>
                        </thead>
                        <tbody id="action-body"></tbody>
                    </table>
                </div>
            </div>

            <!-- Download -->
            <div class="download-row">
                <button class="btn-download" id="download-btn">
                    ⬇️ Download JSON
                </button>
            </div>
        </div>
    </div>

    <script>
        const fileInput   = document.getElementById('file');
        const dropArea    = document.getElementById('drop-area');
        const fileNameEl  = document.getElementById('file-name');
        const analyzeBtn  = document.getElementById('analyze-btn');
        const statusEl    = document.getElementById('status');
        const resultsEl   = document.getElementById('results');
        const successEl   = document.getElementById('success-banner');
        const summaryEl   = document.getElementById('summary');
        const decisionsEl = document.getElementById('decisions');
        const actionHead  = document.getElementById('action-header');
        const actionBody  = document.getElementById('action-body');
        const downloadBtn = document.getElementById('download-btn');

        let lastPayload = null;

        // ── Drag & drop highlight ──
        dropArea.addEventListener('dragover', e => { e.preventDefault(); dropArea.classList.add('dragover'); });
        dropArea.addEventListener('dragleave', () => dropArea.classList.remove('dragover'));
        dropArea.addEventListener('drop', e => {
            e.preventDefault();
            dropArea.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                onFileChosen();
            }
        });

        fileInput.addEventListener('change', onFileChosen);

        function onFileChosen() {
            const f = fileInput.files[0];
            if (f) {
                fileNameEl.textContent = '📎 ' + f.name;
                analyzeBtn.disabled = false;
            } else {
                fileNameEl.textContent = '';
                analyzeBtn.disabled = true;
            }
        }

        // ── Analyze ──
        analyzeBtn.addEventListener('click', async () => {
            const file = fileInput.files[0];
            if (!file) return;

            analyzeBtn.disabled = true;
            statusEl.className = 'status-msg';
            statusEl.innerHTML = '<span class="spinner"></span> Analyzing your transcript…';
            resultsEl.style.display = 'none';
            successEl.style.display = 'none';

            try {
                const formData = new FormData();
                formData.append('file', file);

                const res = await fetch('/api/analyze', { method: 'POST', body: formData });
                const payload = await res.json();

                if (!res.ok) throw new Error(payload.detail || 'Analysis failed.');

                lastPayload = payload;
                renderResults(payload);
                statusEl.textContent = '';
                successEl.style.display = 'flex';
                resultsEl.style.display = 'block';
                resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

            } catch (err) {
                statusEl.className = 'status-msg error';
                statusEl.textContent = '⚠️ ' + err.message;
            } finally {
                analyzeBtn.disabled = false;
            }
        });

        // ── Render structured results ──
        function renderResults(data) {
            // Summary
            const summary = data['Meeting Summary'] || data['summary'] || '';
            summaryEl.textContent = summary;

            // Key Decisions
            decisionsEl.innerHTML = '';
            const decisions = data['Key Decisions'] || data['key_decisions'] || [];
            const decisionArr = Array.isArray(decisions) ? decisions : [decisions];
            decisionArr.forEach(d => {
                const li = document.createElement('li');
                li.textContent = typeof d === 'object' ? JSON.stringify(d) : d;
                decisionsEl.appendChild(li);
            });

            // Action Items table
            actionHead.innerHTML = '';
            actionBody.innerHTML = '';
            const items = data['Action Items'] || data['action_items'] || [];
            if (Array.isArray(items) && items.length > 0) {
                if (typeof items[0] === 'object') {
                    // Object rows → auto-generate columns from keys
                    const keys = Object.keys(items[0]);
                    keys.forEach(k => {
                        const th = document.createElement('th');
                        th.textContent = k;
                        actionHead.appendChild(th);
                    });
                    items.forEach(row => {
                        const tr = document.createElement('tr');
                        keys.forEach(k => {
                            const td = document.createElement('td');
                            td.textContent = row[k] ?? '—';
                            tr.appendChild(td);
                        });
                        actionBody.appendChild(tr);
                    });
                } else {
                    // Plain string list
                    const th = document.createElement('th');
                    th.textContent = 'Action Item';
                    actionHead.appendChild(th);
                    items.forEach(item => {
                        const tr = document.createElement('tr');
                        const td = document.createElement('td');
                        td.textContent = item;
                        tr.appendChild(td);
                        actionBody.appendChild(tr);
                    });
                }
            } else {
                const tr = document.createElement('tr');
                const td = document.createElement('td');
                td.textContent = 'No action items found.';
                td.colSpan = 99;
                td.style.color = 'var(--muted)';
                tr.appendChild(td);
                actionBody.appendChild(tr);
            }
        }

        // ── Download JSON ──
        downloadBtn.addEventListener('click', () => {
            if (!lastPayload) return;
            const blob = new Blob([JSON.stringify(lastPayload, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'meeting_summary.json';
            a.click();
            URL.revokeObjectURL(url);
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return HTML_PAGE


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Please upload a .txt file.")

    transcript = (await file.read()).decode("utf-8")

    try:
        response = analyze_meeting(transcript)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="Groq returned invalid JSON.") from exc

    return JSONResponse(content=data)