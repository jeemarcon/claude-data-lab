# Claude Data Lab

A personal data lab and study space for building AI-powered projects using the Claude API.

## Structure

```
claude-data-lab/
├── projects/
│   └── chat/          # Multi-turn chat with Claude
└── .env.example       # Required environment variables
```

Each project lives in its own folder under `projects/` with its own `requirements.txt` and README.

## Setup

1. Copy `.env.example` to `.env` and fill in your API key:
   ```bash
   cp .env.example .env
   ```

2. Navigate to a project folder and install its dependencies:
   ```bash
   cd projects/chat
   pip install -r requirements.txt
   ```

3. Run the project:
   ```bash
   python chat.py
   ```

## Projects

| Project | Description |
|---------|-------------|
| [chat](projects/chat/) | Interactive multi-turn chat with Claude from the terminal |
