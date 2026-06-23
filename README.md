<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=Travel%20Booking%20Agent&fontSize=50&fontAlignY=35&desc=Multi-Agent%20AI%20Travel%20Planner%20%E2%80%94%20LangGraph%20%E2%80%94%20Groq%20LLM&descAlignY=55" />
</p>

<p align="center">
  <a href="https://travel-booking-agent-3qr7l6euqrkbdneau2wvkq.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Live Demo"/>
  </a>
</p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#project-structure">Structure</a> ·
  <a href="#comparison">Comparison</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/LangGraph-Agentic-blueviolet" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/Groq-llama--3.3--70b-orange" alt="Groq"/>
  <img src="https://img.shields.io/badge/LangChain-Core-important?logo=langchain" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Gemini-2.5%20Flash-yellow" alt="Gemini 2.5 Flash"/>
  <img src="https://img.shields.io/badge/OpenRouter-Routing-purple" alt="OpenRouter"/>
  <img src="https://img.shields.io/badge/Tavily-Search-orange" alt="Tavily"/>
  <img src="https://img.shields.io/badge/AviationStack-Flights-blue" alt="AviationStack"/>
  <img src="https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/PostgreSQL-Checkpoint-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License"/>
</p>

---

Five autonomous LangGraph agents working together — searches flights, finds hotels, builds an itinerary, and emails the plan.

## Features

- **Flight Agent** — AviationStack API searches real-time flight data
- **Hotel Agent** — Tavily web search finds accommodation options
- **Itinerary Agent** — Groq Llama 3.3 70B builds a day-by-day travel plan
- **Final Agent** — Compiles everything into a polished summary
- **Email Agent** — SMTP delivers the itinerary to any email address
- **PostgreSQL Checkpointer** — Persists conversation state across sessions
- **Streamlit UI** — Dark-themed interface with live agent pipeline streaming

## Architecture

```mermaid
flowchart LR
  User["🙋 User Query"] --> Flight["✈️ Flight Agent<br/>(AviationStack)"]
  Flight --> Hotel["🏨 Hotel Agent<br/>(Tavily)"]
  Hotel --> Itinerary["🗓️ Itinerary Agent<br/>(Groq Llama 3.3)"]
  Itinerary --> Final["🧠 Final Agent<br/>(Groq Llama 3.3)"]
  Final --> Email["📬 Email Agent<br/>(SMTP)"]
  Email --> Plan["✅ Travel Plan Delivered"]
```

| Agent | Tool / API | Output |
|---|---|---|
| **Flight Agent** | AviationStack API | Real-time flight data |
| **Hotel Agent** | Tavily Search | Hotel & accommodation info |
| **Itinerary Agent** | Groq Llama 3.3 70B | Day-by-day travel itinerary |
| **Final Agent** | Groq Llama 3.3 70B | Polished final summary |
| **Email Agent** | Gmail SMTP | Itinerary emailed to recipient |

## Quick Start

```bash
git clone https://github.com/kairav7220/travel-booking-agent.git
cd travel-booking-agent
pip install -r requirements.txt
```

Set your API keys in `.env`:

```env
GROQ_API_KEY="gsk_..."
TAVILY_API_KEY="tvly-..."
AVIATIONSTACK_API_KEY="..."
DATABASE_URL="postgresql://user:pass@host:5432/travel_agent"
EMAIL_ADDRESS="your@gmail.com"
EMAIL_PASSWORD="gmail-app-password"
```

```bash
streamlit run frontend.py
```

## Usage

1. Open the Streamlit app in your browser
2. Describe your trip (e.g. "7-day Japan trip under ₹2 lakhs")
3. Enter recipient email for the itinerary
4. Watch the 5-agent pipeline run live
5. Download or auto-save the final travel plan

## Comparison

| Feature | Travel Booking Agent | Manual Booking | Basic Chatbot |
|---|---|---|---|
| Agents | 5 (flight + hotel + itinerary + final + email) | — | 1 |
| Flight Search | ✅ AviationStack API | ✅ | ❌ |
| Hotel Search | ✅ Tavily | ✅ | ❌ |
| AI Itinerary | ✅ Groq LLM | ❌ | ✅ |
| Email Delivery | ✅ SMTP | ❌ | ❌ |
| State Persistence | ✅ PostgreSQL checkpointer | — | ❌ |
| UI | ✅ Streamlit (dark theme) | — | ✅ |

## Project Structure

```
travel-booking-agent/
├── frontend.py              # Streamlit UI (dark theme, agent pipeline streaming)
├── main.py                  # LangGraph graph (5 agents + PostgreSQL checkpointer)
├── requirements.txt         # Python dependencies
├── tools/
│   ├── flight_tool.py       # AviationStack API wrapper
│   └── tavily_tool.py       # Tavily search wrapper
├── CONTRIBUTING.md          # Contribution guide
├── llms.txt                 # AI assistant context
├── .gitignore
├── LICENSE
└── README.md
```

## License

MIT © [kairav7220](https://github.com/kairav7220)

---

<p align="center">
  Built with <a href="https://langchain-ai.github.io/langgraph">LangGraph</a> ·
  <a href="https://groq.com">Groq</a> ·
  <a href="https://tavily.com">Tavily</a> ·
  <a href="https://aviationstack.com">AviationStack</a> ·
  <a href="https://streamlit.io">Streamlit</a> ·
  <a href="https://www.postgresql.org">PostgreSQL</a>
</p>
