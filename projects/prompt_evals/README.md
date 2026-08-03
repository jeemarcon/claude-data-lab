# Prompt Evals

Conjunto de experimentos para avaliação de prompts usando o Claude como juiz (LLM-as-a-judge).

## Files

| File | Description |
|------|-------------|
| `prompt_eval.py` | Gera dataset de tarefas AWS e salva em `docs/dataset.json` |
| `prompt_eval_grader.py` | Gera dataset com critérios, executa cada tarefa e salva resultados em `docs/` |
| `prompt_engineer.py` | `PromptEvaluator` — classe com geração de dataset e avaliação concorrente; salva relatório HTML em `docs/` |
| `prompt_eval_from_zero.py` | Avaliador simples construído do zero: executa um prompt, avalia a saída e salva relatório HTML |
| `app.py` | Servidor Flask com interface web — recebe o prompt via browser e exibe a avaliação dinamicamente |

## How to run

```bash
# Gerar dataset de tarefas AWS e avaliar
python prompt_eval.py
python prompt_eval_grader.py

# Avaliador com PromptEvaluator (execução concorrente + relatório HTML)
python prompt_engineer.py

# Avaliador simples — salva docs/eval_report.html
python prompt_eval_from_zero.py

# Interface web (acesse http://localhost:5001)
python app.py
```

## Output

Todos os arquivos gerados ficam em `docs/`:

| File | Description |
|------|-------------|
| `docs/dataset.json` | Dataset gerado por `prompt_eval.py` |
| `docs/dataset2.json` | Dataset com critérios gerado por `prompt_eval_grader.py` |
| `docs/results.json` | Resultados da avaliação do `prompt_eval_grader.py` |
| `docs/output.json` | Resultados da avaliação do `prompt_engineer.py` |
| `docs/output.html` | Relatório HTML do `prompt_engineer.py` |
| `docs/eval_report.html` | Relatório HTML do `prompt_eval_from_zero.py` |
