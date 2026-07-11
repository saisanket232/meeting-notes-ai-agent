import json
from html import escape

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from agents.meeting_agent import analyze_meeting


app = FastAPI(title="AI Meeting Notes Agent")


def render_page(result_json: str = "") -> str:
    escaped_result = escape(result_json)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>AI Meeting Notes Agent</title>
        <style>
            :root {{
                color-scheme: dark;
                --bg: #0b0f14;
                --card: #121826;
                --accent: #4f8cff;
                --accent-2: #7dd3fc;
                --text: #e5eefb;
                --muted: #a8b3c7;
                --border: #22304a;
            }}
            body {{
                margin: 0;
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                background: radial-gradient(circle at top, #132036 0%, var(--bg) 45%);
                color: var(--text);
            }}
            .wrap {{
                max-width: 980px;
                margin: 0 auto;
                padding: 48px 20px 64px;
            }}
            .hero {{
                text-align: center;
                margin-bottom: 28px;
            }}
            .hero h1 {{
                margin: 0 0 12px;
                font-size: clamp(2rem, 5vw, 3.5rem);
            }}
            .hero p {{
                margin: 0 auto;
                max-width: 720px;
                color: var(--muted);
                line-height: 1.6;
            }}
            .grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            .card {{
                background: rgba(18, 24, 38, 0.88);
                border: 1px solid var(--border);
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
                padding: 24px;
                backdrop-filter: blur(14px);
            }}
            .upload {{
                display: grid;
                gap: 14px;
                justify-items: center;
                text-align: center;
            }}
            .upload input[type="file"] {{
                width: min(100%, 440px);
                padding: 14px;
                border: 1px dashed var(--border);
                border-radius: 14px;
                background: rgba(255, 255, 255, 0.03);
                color: var(--muted);
            }}
            .btn {{
                border: 0;
                border-radius: 999px;
                padding: 12px 22px;
                font-weight: 700;
                color: white;
                background: linear-gradient(135deg, var(--accent), var(--accent-2));
                cursor: pointer;
            }}
            .btn:disabled {{
                opacity: 0.65;
                cursor: not-allowed;
            }}
            .hint {{
                color: var(--muted);
                font-size: 0.95rem;
            }}
            pre {{
                margin: 0;
                overflow: auto;
                white-space: pre-wrap;
                word-break: break-word;
                background: #0a0f18;
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 18px;
                min-height: 220px;
            }}
            .status {{
                min-height: 24px;
                color: var(--accent-2);
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <section class="hero">
                <h1>AI Meeting Notes Agent</h1>
                <p>Upload a meeting transcript, let Groq extract the summary, decisions, and action items, then download or copy the structured JSON result.</p>
            </section>

            <div class="grid">
                <section class="card upload">
                    <h2>Upload Meeting Transcript</h2>
                    <input id="file" type="file" accept=".txt" />
                    <button id="analyze" class="btn">Analyze Meeting</button>
                    <div id="status" class="status"></div>
                    <div class="hint">Supported format: .txt</div>
                </section>

                <section class="card">
                    <h2>Results</h2>
                    <pre id="output">{escaped_result}</pre>
                </section>
            </div>
        </div>

        <script>
            const fileInput = document.getElementById('file');
            const button = document.getElementById('analyze');
            const output = document.getElementById('output');
            const status = document.getElementById('status');

            button.addEventListener('click', async () => {{
                const file = fileInput.files[0];
                if (!file) {{
                    status.textContent = 'Please choose a .txt file first.';
                    return;
                }}

                button.disabled = true;
                status.textContent = 'Analyzing...';
                output.textContent = '';

                try {{
                    const formData = new FormData();
                    formData.append('file', file);

                    const response = await fetch('/api/analyze', {{
                        method: 'POST',
                        body: formData
                    }});

                    const payload = await response.json();

                    if (!response.ok) {{
                        throw new Error(payload.detail || 'Analysis failed');
                    }}

                    output.textContent = JSON.stringify(payload, null, 2);
                    status.textContent = 'Analysis complete.';
                }} catch (error) {{
                    output.textContent = '';
                    status.textContent = error.message;
                }} finally {{
                    button.disabled = false;
                }}
            }});
        </script>
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return render_page()


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