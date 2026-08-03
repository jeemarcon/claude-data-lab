from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5"


# ──────────────────────────────────────────────
# 1. EXECUÇÃO DO PROMPT
# ──────────────────────────────────────────────

def run_prompt(prompt: str) -> str:
    """Envia o prompt para o modelo e retorna a resposta gerada."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


# ──────────────────────────────────────────────
# 2. AVALIAÇÃO DA SAÍDA
# ──────────────────────────────────────────────

def evaluate_output(prompt: str, output: str) -> dict:
    """
    Usa o modelo como juiz para avaliar a saída gerada pelo prompt.

    Retorna um dicionário com:
    - context:    resumo do que o prompt solicitou
    - score:      nota de 1 a 10
    - motivation: justificativa detalhada da nota
    """
    eval_prompt = f"""
You are an expert prompt evaluator. Your job is to analyze a prompt and its generated output, then provide a structured evaluation.

<prompt>
{prompt}
</prompt>

<output>
{output}
</output>

Evaluate the output considering:
1. **Precision** — Was the answer accurate and to the point?
2. **Ambiguity** — Did the output have conflicting or dual interpretations?
3. **Examples** — When relevant, were examples provided or missing?
4. **Specificity** — Was the output specific enough, or too generic?
5. **Completeness** — Did it fully address what the prompt requested?

Respond ONLY with a JSON object in this exact shape:
{{
    "context": "A 1-2 sentence summary of what the prompt asked for",
    "score": <integer from 1 to 10>,
    "motivation": "A paragraph explaining the score: what was good, what was missing, and what could be improved"
}}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": eval_prompt},
            {"role": "assistant", "content": "```json"},
        ],
        stop_sequences=["```"],
    )

    return json.loads(response.content[0].text)


# ──────────────────────────────────────────────
# 3. GERAÇÃO DO RELATÓRIO HTML
# ──────────────────────────────────────────────

def score_color(score: int) -> tuple[str, str]:
    """Retorna (background, text) color baseado na nota."""
    if score >= 8:
        return "#c8e6c9", "#2e7d32"
    elif score >= 5:
        return "#fff9c4", "#f57f17"
    else:
        return "#ffcdd2", "#c62828"


def generate_html_report(prompt: str, output: str, evaluation: dict) -> str:
    """
    Gera uma página HTML com o relatório completo da avaliação.

    Seções:
    - Contexto do prompt
    - Saída gerada
    - Nota (com cor indicativa)
    - Motivação da nota
    """
    score = evaluation["score"]
    bg_color, text_color = score_color(score)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Evaluation Report</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            color: #333;
            padding: 40px 20px;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 32px;
            font-size: 1.8rem;
            color: #222;
        }}
        .card {{
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 24px 28px;
            margin-bottom: 20px;
            max-width: 860px;
            margin-left: auto;
            margin-right: auto;
        }}
        .card h2 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #888;
            margin-bottom: 12px;
        }}
        .card p, .card pre {{
            font-size: 0.95rem;
            line-height: 1.7;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        pre {{
            background: #f8f8f8;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 14px;
            font-family: 'Courier New', monospace;
            font-size: 0.88rem;
        }}
        .score-badge {{
            display: inline-block;
            font-size: 2.2rem;
            font-weight: bold;
            padding: 12px 28px;
            border-radius: 8px;
            background-color: {bg_color};
            color: {text_color};
        }}
        .score-label {{
            display: inline-block;
            margin-left: 12px;
            font-size: 0.95rem;
            color: #666;
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <h1>Prompt Evaluation Report</h1>

    <div class="card">
        <h2>Contexto do Prompt</h2>
        <p>{evaluation["context"]}</p>
    </div>

    <div class="card">
        <h2>Prompt Inserido</h2>
        <pre>{prompt}</pre>
    </div>

    <div class="card">
        <h2>Saída Gerada</h2>
        <pre>{output}</pre>
    </div>

    <div class="card">
        <h2>Nota</h2>
        <span class="score-badge">{score}/10</span>
        <span class="score-label">{'Excelente' if score >= 8 else 'Satisfatório' if score >= 5 else 'Insuficiente'}</span>
    </div>

    <div class="card">
        <h2>Motivação da Nota</h2>
        <p>{evaluation["motivation"]}</p>
    </div>
</body>
</html>"""


# ──────────────────────────────────────────────
# 4. PONTO DE ENTRADA
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # Prompt de exemplo — substitua pelo que quiser avaliar
    prompt = """
    Create a meal plan for a 30 years active women.
    """

    print("Running prompt...")
    output = run_prompt(prompt)

    print("Evaluating output...")
    evaluation = evaluate_output(prompt, output)

    docs_dir = Path(__file__).parent / "docs"
    docs_dir.mkdir(exist_ok=True)

    html = generate_html_report(prompt, output, evaluation)
    report_path = docs_dir / "eval_report.html"
    report_path.write_text(html, encoding="utf-8")

    print(f"\nScore: {evaluation['score']}/10")
    print(f"Motivation: {evaluation['motivation']}")
    print(f"\nHTML report saved to: {report_path}")
