from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import asyncio
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters, ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.6,
)

server_parameters = StdioServerParameters(
    command="npx.cmd",
    env={
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")
    },
    args=["firecrawl-mcp"]
)


async def main():
    async with stdio_client(server_parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session=session)
            agent = create_react_agent(llm, tools)

            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites, crawl pages, and extract data using Firecrawl tools. Think step by step and use the appropriate tools to help the user."

                }
            ]

            print('Available Tools: - ', *[tool.name for tool in tools])
            print("-" * 60)

            while True:
                user_input = input("\nYou: ")
                if user_input == "quit":
                    print("GoodBye")
                    break

                message.append({"role": "user", "content": user_input[:175000]})

                try:
                    agent_response = await agent.ainvoke({"messages": message})
                    ai_message = agent_response["messages"][-1].content
                    print("\nAgent: ", ai_message)
                except Exception as e:
                    print("Error: ", e)


if __name__ == "__main__":
    asyncio.run(main())
