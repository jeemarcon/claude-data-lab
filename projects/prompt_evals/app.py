"""
Servidor Flask que expõe a avaliação de prompts via API REST.

Rotas:
  GET  /           → serve a página HTML com o formulário
  POST /evaluate   → recebe { "prompt": "..." }, executa e avalia, retorna JSON
"""

from flask import Flask, request, jsonify
from prompt_eval_from_zero import run_prompt, evaluate_output

app = Flask(__name__)


# ──────────────────────────────────────────────
# FRONTEND — página HTML servida pelo Flask
# ──────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Evaluator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            color: #333;
            padding: 40px 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 8px;
            font-size: 1.8rem;
            color: #222;
        }
        .subtitle {
            text-align: center;
            color: #888;
            font-size: 0.9rem;
            margin-bottom: 32px;
        }
        .card {
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 24px 28px;
            margin-bottom: 20px;
            max-width: 860px;
            margin-left: auto;
            margin-right: auto;
        }
        .card h2 {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #888;
            margin-bottom: 12px;
        }
        .card p, .card pre {
            font-size: 0.95rem;
            line-height: 1.7;
        }
        pre {
            background: #f8f8f8;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 14px;
            font-family: 'Courier New', monospace;
            font-size: 0.88rem;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 12px;
            font-size: 0.95rem;
            font-family: Arial, sans-serif;
            border: 1px solid #ddd;
            border-radius: 6px;
            resize: vertical;
            line-height: 1.6;
            outline: none;
            transition: border-color 0.2s;
        }
        textarea:focus { border-color: #555; }
        button {
            display: block;
            width: 100%;
            margin-top: 12px;
            padding: 12px;
            font-size: 1rem;
            font-weight: bold;
            background: #333;
            color: #fff;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover:not(:disabled) { background: #555; }
        button:disabled { background: #aaa; cursor: not-allowed; }
        .score-badge {
            display: inline-block;
            font-size: 2.2rem;
            font-weight: bold;
            padding: 12px 28px;
            border-radius: 8px;
        }
        .score-label {
            display: inline-block;
            margin-left: 12px;
            font-size: 0.95rem;
            color: #666;
            vertical-align: middle;
        }
        .score-high  { background: #c8e6c9; color: #2e7d32; }
        .score-mid   { background: #fff9c4; color: #f57f17; }
        .score-low   { background: #ffcdd2; color: #c62828; }
        #results { display: none; }
        .spinner {
            display: none;
            text-align: center;
            padding: 20px;
            color: #888;
            font-size: 0.9rem;
            max-width: 860px;
            margin: 0 auto;
        }
        .spinner.active { display: block; }
        .error-msg {
            background: #ffcdd2;
            color: #c62828;
            border-radius: 8px;
            padding: 14px 20px;
            max-width: 860px;
            margin: 0 auto 20px;
            display: none;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <h1>Prompt Evaluator</h1>
    <p class="subtitle">Insira um prompt, clique em Avaliar e veja a análise gerada pelo modelo.</p>

    <!-- Formulário de entrada -->
    <div class="card">
        <h2>Seu Prompt</h2>
        <textarea id="prompt-input" placeholder="Digite o prompt que deseja avaliar..."></textarea>
        <button id="evaluate-btn">Avaliar</button>
    </div>

    <!-- Loading -->
    <div class="spinner" id="spinner">Executando e avaliando o prompt... aguarde.</div>

    <!-- Erro -->
    <div class="error-msg" id="error-msg"></div>

    <!-- Resultados (ocultos até a avaliação retornar) -->
    <div id="results">
        <div class="card">
            <h2>Contexto do Prompt</h2>
            <p id="res-context"></p>
        </div>
        <div class="card">
            <h2>Saída Gerada</h2>
            <pre id="res-output"></pre>
        </div>
        <div class="card">
            <h2>Nota</h2>
            <span class="score-badge" id="res-score-badge"></span>
            <span class="score-label" id="res-score-label"></span>
        </div>
        <div class="card">
            <h2>Motivação da Nota</h2>
            <p id="res-motivation"></p>
        </div>
    </div>

    <script>
        async function runEvaluation() {
            const promptText = document.getElementById("prompt-input").value.trim();
            if (!promptText) {
                showError("Por favor, insira um prompt antes de avaliar.");
                return;
            }

            setLoading(true);
            hideError();
            document.getElementById("results").style.display = "none";

            try {
                const response = await fetch("/evaluate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ prompt: promptText }),
                });

                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || "Erro desconhecido.");
                }

                const data = await response.json();
                renderResults(data);
            } catch (err) {
                showError("Erro ao avaliar: " + err.message);
            } finally {
                setLoading(false);
            }
        }

        function renderResults({ prompt, output, evaluation }) {
            const score = evaluation.score;

            document.getElementById("res-context").textContent = evaluation.context;
            document.getElementById("res-output").textContent = output;
            document.getElementById("res-motivation").textContent = evaluation.motivation;

            const badge = document.getElementById("res-score-badge");
            badge.textContent = score + "/10";
            badge.className = "score-badge " + (score >= 8 ? "score-high" : score >= 5 ? "score-mid" : "score-low");

            document.getElementById("res-score-label").textContent =
                score >= 8 ? "Excelente" : score >= 5 ? "Satisfatório" : "Insuficiente";

            document.getElementById("results").style.display = "block";
            document.getElementById("results").scrollIntoView({ behavior: "smooth" });
        }

        function setLoading(active) {
            document.getElementById("spinner").className = active ? "spinner active" : "spinner";
            document.getElementById("evaluate-btn").disabled = active;
            document.getElementById("evaluate-btn").textContent = active ? "Avaliando..." : "Avaliar";
        }

        function showError(msg) {
            const el = document.getElementById("error-msg");
            el.textContent = msg;
            el.style.display = "block";
        }

        function hideError() {
            document.getElementById("error-msg").style.display = "none";
        }

        document.addEventListener("DOMContentLoaded", function () {
            document.getElementById("evaluate-btn").addEventListener("click", runEvaluation);
        });
    </script>
</body>
</html>"""


# ──────────────────────────────────────────────
# ROTAS
# ──────────────────────────────────────────────

@app.route("/")
def index():
    """Serve a página com o formulário de avaliação."""
    return HTML


@app.route("/evaluate", methods=["POST"])
def evaluate():
    """
    Recebe { "prompt": "..." } via POST JSON.
    Executa o prompt no modelo, avalia a saída e retorna:
    { "prompt", "output", "evaluation": { context, score, motivation } }
    """
    data = request.get_json(silent=True)
    if not data or not data.get("prompt", "").strip():
        return jsonify({"error": "Campo 'prompt' é obrigatório."}), 400

    prompt = data["prompt"].strip()

    try:
        output = run_prompt(prompt)
        evaluation = evaluate_output(prompt, output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"prompt": prompt, "output": output, "evaluation": evaluation})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
