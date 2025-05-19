from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

#web search agent
websearch_agent = Agent(
    name = "Web search Agent",
    role = "Search the web for the information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools = [DuckDuckGo()],
    instructions=["Always include source"],
    show_tool_calls= True,
    markdown=True

)
#finance agent
finance_agent = Agent(
    name = "Finance AI Agent",
    role = "agent to access stock data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools = [YFinanceTools(stock_price = True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True

)

multi_model_agent = Agent(
    team=[websearch_agent,finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Always include source","Use tables to display the data"],
    show_tool_calls=True,
    markdown=True
)

# multi_model_agent.print_response("Summarize analyst recommendation and share the latest news for NVDA", stream=True)

if __name__ == "__main__":
    # Code to ensure the script runs only when executed directly
    print("Running the financial agent script directly.")
    multi_model_agent.print_response("Summarize analyst recommendation and share the latest news for NVDA", stream=True)