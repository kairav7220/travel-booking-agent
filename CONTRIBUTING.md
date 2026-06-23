# Contributing

## Setup

```bash
git clone https://github.com/kairav7220/travel-booking-agent.git
cd travel-booking-agent
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your API keys.

## Guidelines

- Keep agents modular — each agent in `main.py` should have a single responsibility
- Add new tools under `tools/` following the existing pattern
- Run `streamlit run frontend.py` to test UI changes
- Format Python code with `ruff` before committing

## Adding an Agent

1. Define a new node function in `main.py` that accepts and returns `TravelState`
2. Add the node to the graph with `graph.add_node()`
3. Wire it into the pipeline with `graph.add_edge()`
4. Add a status card in `frontend.py` under `AGENT_META`

## Commit Messages

Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`
