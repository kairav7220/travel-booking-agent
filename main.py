import os
import psycopg
import operator
import smtplib
from email.message import EmailMessage
from typing import TypedDict, Annotated
from langchain_community.utilities import SQLDatabase

# SystemMessage: Gives Instructions rules to AI.
# HumanMessage: Represent the message sent by user.
# AIMessage: Represents the message sent by AI model.
# AnyMessage: Can represent any type of message.
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openrouter import ChatOpenRouter

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
llm = ChatGroq(model='llama-3.3-70b-versatile')

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    recipient_email: str
    llm_calls: int

# Flight agent to search for flights based on user query using AviationStack API
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel agent to search for hotels based on user query using Tavily API.
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_data = tavily_search(query)
    return {
        "hotel_results": hotel_data,
        "messages": [
            AIMessage(content=f"Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary agent to create a travel itinerary based on flight agent and hotel agent outputs.
def itinerary_agent(state: TravelState):
    prompt = f"""
    Create a travel itinerary.
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}
    """

    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner"),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
def email_agent(state: TravelState):
    final_plan = state.get("itinerary", "No itinerary found.")
    
    to_address = state.get("recipient_email", EMAIL_ADDRESS)
    if not to_address:
        return {"messages": [AIMessage(content="Email skipped: No recipient address provided.")]}
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            msg = EmailMessage()
            msg['Subject'] = f"Your Planned Trip Itinerary: {state['user_query']}"
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to_address
            msg.set_content(final_plan)
            server.send_message(msg)
        return {
            "messages": [AIMessage(content=f"Successfully emailed the itinerary to {to_address} ✅")]
        }
    except Exception as e:
        return {
            "messages": [AIMessage(content=f"Failed to send email. Error: {str(e)} ⚠️")]
        }

# Final agent to compile all information and generate final response
def final_agent(state: TravelState):
    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}
    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "itinerary": response.content, 
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)
graph.add_node("email_agent", email_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", "email_agent")
graph.add_edge("email_agent", END)

_conn = psycopg.connect(DATABASE_URL)
_conn.autocommit = True
checkpointer = PostgresSaver(_conn)
checkpointer.setup()
_conn.autocommit = False
app = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    config = {
        'configurable': { 'thread_id': 'user_aarohi' }
    }

    user_input = input('Enter travel request: ')
    email_input = input('Enter recipient email: ').strip()
    
    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "recipient_email": email_input,
            "llm_calls": 0
        },
        config=config
    )

    print("\nFINAL RESPONSE\n")

    if result.get('itinerary'):
        print(result['itinerary'])
    else:
        print("No itinerary text found in state.")


    if result.get('itinerary'):
        print(result['itinerary'])
    else:
        print("No itinerary text found in state.")

    print("\n" + "="*50)
    print("           EMAIL STATUS")
    print("="*50 + "\n")
    
    if result['messages']:
        print(result['messages'][-1].content)