import pandas as pd

from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


def query_agent(data: bytes, query: str) -> str:
    df = pd.read_csv(data)
    llm = OpenAI()
    agent = create_pandas_dataframe_agent(llm, df)
    return agent.invoke(query)
