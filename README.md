# Claude Data Lab

A personal data lab and study space for building AI-powered projects using the Claude API.

## Structure

```
claude-data-lab/
├── projects/
│   ├── chat/          # Multi-turn chat with Claude
│   └── prompt_evals/  # LLM-as-a-judge prompt evaluation
└── .env.example       # Required environment variables
```

Each project lives in its own folder under `projects/`. Dependencies are shared via the root `requirements.txt`.

## Setup

1. Copy `.env.example` to `.env` and fill in your API key:
   ```bash
   cp .env.example .env
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run a project:
   ```bash
   python projects/chat/chat.py
   ```

## Projects

| Project | Description |
|---------|-------------|
| [chat](projects/chat/) | Interactive multi-turn chat with Claude from the terminal |
| [prompt_evals](projects/prompt_evals/) | LLM-as-a-judge evaluation of prompts for AWS tasks (Python, JSON, Regex) |
