"""天气预报 AI Agent 示例.

这是一个基于 LangChain v1 的简单 AI Agent 示例，演示了：
- 系统提示词定义
- 工具（Tool）的创建和使用
- 运行时上下文（Runtime Context）
- 结构化输出（Structured Output）
- 对话记忆（Conversational Memory）
"""

import os
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_qwq import ChatQwen
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import get_runtime

# ==================== 系统提示词 ====================

SYSTEM_PROMPT = """你是一位专业的天气预报员，喜欢使用双关语。

你可以使用两个工具：

- get_weather_for_location: 用于获取特定位置的天气信息
- get_user_location: 用于获取用户的位置

如果用户询问天气，请确保你知道位置。如果从问题中可以判断用户指的是他们所在的位置，
请使用 get_user_location 工具来获取他们的位置。"""


# ==================== 上下文定义 ====================


@dataclass
class Context:
    """自定义运行时上下文模式."""

    user_id: str


# ==================== 工具定义 ====================


@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气信息."""
    return f"{city} 总是阳光明媚！"


@tool
def get_user_location() -> str:
    """根据用户 ID 获取用户位置信息."""
    runtime = get_runtime(Context)
    user_id = runtime.context.user_id
    return "佛罗里达" if user_id == "1" else "旧金山"


# ==================== 响应格式定义 ====================


@dataclass
class ResponseFormat:
    """Agent 的响应模式."""

    # 带有双关语的回复（必填）
    punny_response: str
    # 如果有的话，包含有趣的天气信息（可选）
    weather_conditions: str | None = None


# ==================== 模型配置 ====================

model = ChatQwen(
    model="qwen3-next-80b-a3b-instruct",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.5,
    max_tokens=1000,
)


# ==================== 检查点配置 ====================

# 使用内存检查点保存对话状态
checkpointer = InMemorySaver()


# ==================== 创建 Agent ====================

graph = create_agent(
    model=model,
    prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    # checkpointer=checkpointer,
)
