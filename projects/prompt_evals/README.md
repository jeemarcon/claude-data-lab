# Prompt Evals

Avalia a qualidade de respostas geradas pelo Claude usando um modelo como juiz (LLM-as-a-judge).

O projeto foca em tarefas AWS que exigem Python, JSON ou Regex. O dataset é gerado automaticamente pelo próprio Claude, e cada resposta é avaliada por um segundo modelo que atribui pontuação e justificativa.

## Files

| File | Description |
|------|-------------|
| `prompt_eval.py` | Gera o dataset de tarefas e salva em `docs/dataset.json` |
| `prompt_eval_grader.py` | Gera dataset com critérios de solução, executa cada tarefa e salva os resultados em `docs/` |

## How it works

```
generate_dataset()
    └── Claude gera N tarefas no formato JSON (task, format, solution_criteria)

run_eval(dataset)
    └── para cada tarefa:
        ├── run_prompt()       → Claude resolve a tarefa
        └── grade_by_model()   → Claude avalia a solução (score 1-10 + strengths/weaknesses)
```

## Run

```bash
# Apenas gerar o dataset
python prompt_eval.py

# Gerar dataset, rodar avaliação e salvar resultados
python prompt_eval_grader.py
```

## Output

Os arquivos gerados ficam em `docs/`:

| File | Description |
|------|-------------|
| `docs/dataset.json` | Dataset de tarefas gerado por `prompt_eval.py` |
| `docs/dataset2.json` | Dataset com critérios gerado por `prompt_eval_grader.py` |
| `docs/results.json` | Resultados da avaliação com score e reasoning por tarefa |

## Result shape

```json
[
  {
    "output": "solução gerada pelo Claude",
    "test_case": { "task": "...", "format": "...", "solution_criteria": "..." },
    "score": 8,
    "reasoning": "..."
  }
]
```
