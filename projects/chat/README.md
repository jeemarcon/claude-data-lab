# Chat

Interactive multi-turn chat with Claude running in the terminal.

## Setup

```bash
pip install -r ../../requirements.txt
```

## Files

| File | Description |
|------|-------------|
| `chat.py` | Multi-turn chat — mantém histórico da conversa entre as mensagens |
| `chat_stream.py` | Mesma ideia, mas recebe a resposta em streaming (token a token) |

## Run

```bash
# Chat padrão
python chat.py

# Chat com streaming
python chat_stream.py
```

## chat() parameters

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `messages` | `list` | — | Histórico da conversa no formato `[{"role": ..., "content": ...}]` |
| `system` | `str` | `None` | System prompt para configurar o comportamento do modelo |
| `temperature` | `float` | `0.0` | Controla a criatividade da resposta (0.0 = determinístico, 1.0 = mais criativo) |
