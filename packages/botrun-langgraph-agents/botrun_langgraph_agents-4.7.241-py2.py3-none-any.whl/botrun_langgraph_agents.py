import argparse
import asyncio
import functools
import json
import operator
import sys
from typing import Annotated, Sequence, TypedDict, Any, Dict, List

from botrun_google_docs_reader import botrun_google_docs_reader
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core._api import LangChainBetaWarning
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# 載入環境變數
load_dotenv()

import warnings

warnings.filterwarnings("ignore", category=LangChainBetaWarning)


# 定義代理人的狀態類別
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


# 創建代理人的函數
def create_agent(llm: ChatOpenAI, tools: List[Any], system_prompt: str) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor


# 代理人節點執行函數
def agent_node(state: AgentState, agent: AgentExecutor, name: str) -> Dict[str, List[HumanMessage]]:
    print(f"\n\n😊Starting node: {name}")
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}


# 主函數
def botrun_langgraph_agents(user_input_prompt: str, agent_config_path: str) -> None:
    # 初始化 OpenAI 模型
    llm = ChatOpenAI(model="gpt-4o")

    # 初始化工具
    tavily_tool = TavilySearchResults(max_results=3)

    agents_config = read_agents_config(agent_config_path)

    agents = {}
    for agent_info in agents_config:
        agent_name = agent_info["name"]
        agent_prompt = agent_info["prompt"]
        agents[agent_name] = create_agent(llm, [tavily_tool], agent_prompt)

    # 定義代理人節點
    agent_nodes = {name: functools.partial(agent_node, agent=agent, name=name) for name, agent in agents.items()}

    # 監督者定義
    agent_names = list(agents.keys())
    AGENT_SUPERVISOR = "agent_supervisor"
    system_prompt = (
        "你是監督者，負責管理以下工作者的對話：{members}。根據以下用戶請求，"
        "選擇下一個行動的工作者。每個工作者將執行一項任務並回報結果和狀態。"
        "完成後，回應 'FINISH'。"
    )
    options = ["FINISH"] + agent_names
    function_def = {
        "name": "route",
        "description": "Select the next role.",
        "parameters": {
            "title": "routeSchema",
            "type": "object",
            "properties": {
                "next": {
                    "title": "Next",
                    "anyOf": [{"enum": options}],
                }
            },
            "required": ["next"],
        },
    }
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(agent_names))

    supervisor_chain = (
            prompt
            | llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
    )

    # 構建工作流
    workflow = StateGraph(AgentState)
    for name, node in agent_nodes.items():
        workflow.add_node(name, node)
    workflow.add_node(AGENT_SUPERVISOR, supervisor_chain)

    # 添加工作流節點邊
    for member in agent_names:
        workflow.add_edge(member, AGENT_SUPERVISOR)
    conditional_map = {k: k for k in agent_names}
    conditional_map["FINISH"] = END
    workflow.add_conditional_edges(AGENT_SUPERVISOR, lambda x: x["next"], conditional_map)
    workflow.set_entry_point(AGENT_SUPERVISOR)

    graph = workflow.compile()

    # 執行工作流並串流輸出
    async def run_graph_with_stream() -> None:
        async for event in graph.astream_events({"messages": [HumanMessage(content=user_input_prompt)]}, version="v2"):
            kind = event["event"]
            if kind == "on_chain_start":
                if event["name"] == "Agent":
                    print(f"Starting agent: {event['name']} with input: {event['data'].get('input')}")
            elif kind == "on_chain_end":
                if event["name"] == "Agent":
                    print()
                    print("--")
                    print(f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}")
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="")
            elif kind == "on_tool_start":
                print("--")
                print(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")
            elif kind == "on_tool_end":
                print(f"Done tool: {event['name']}")
                print(f"Tool output was: {event['data'].get('output')}")
                print("--")
            sys.stdout.flush()

    asyncio.run(run_graph_with_stream())


def read_agents_config(agent_config_path: str) -> List[Dict[str, Any]]:
    if agent_config_path.startswith("https://docs.google.com/document/d/"):
        doc_id = agent_config_path.split('/')[5]
        content = botrun_google_docs_reader(doc_id)
        agents_config = json.loads(content)
    else:
        # 讀取本地文件內容
        with open(agent_config_path, 'r', encoding='utf-8') as f:
            agents_config = json.load(f)
    return agents_config


# 解析命令行參數並執行主函數
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LangGraph Multi-Agent CLI")
    parser.add_argument(
        "--user_input_prompt",
        type=str,
        default="請幫我寫一篇一百字的 RAG for AI LLM介紹，極短的，不要太長。",
        help="用戶輸入的提示"
    )
    parser.add_argument(
        "--agent_config_path",
        type=str,
        default="https://docs.google.com/document/d/1JZMMOl1lRy0T_1C-cQGg3JSprrsrLazdqIho_G84uIk/",
        help="代理人配置文件的路徑"
    )
    args = parser.parse_args()
    botrun_langgraph_agents(args.user_input_prompt, args.agent_config_path)
