import pytest

from agent.graph import Context, ResponseFormat, graph

pytestmark = pytest.mark.anyio


@pytest.mark.langsmith
async def test_agent_weather_query() -> None:
    """测试 Agent 询问天气的功能."""
    # thread_id 是给定对话的唯一标识符
    config = {"configurable": {"thread_id": "1"}}
    
    # 第一轮对话：询问天气
    response = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "外面天气怎么样？"}]},
        config=config,
        context=Context(user_id="1"),
    )
    
    assert response is not None
    assert "structured_response" in response
    structured = response["structured_response"]
    assert isinstance(structured, ResponseFormat)
    assert structured.punny_response is not None
    assert structured.weather_conditions is not None


@pytest.mark.langsmith
async def test_agent_conversation_memory() -> None:
    """测试 Agent 的对话记忆功能（连续对话）."""
    # 使用相同的 thread_id 保持对话上下文
    config = {"configurable": {"thread_id": "2"}}
    context = Context(user_id="1")
    
    # 第一轮对话：询问天气
    response1 = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "外面天气怎么样？"}]},
        config=config,
        context=context,
    )
    
    assert response1 is not None
    structured1 = response1["structured_response"]
    assert isinstance(structured1, ResponseFormat)
    assert structured1.weather_conditions is not None
    
    # 第二轮对话：表示感谢（应该能记住之前的对话）
    response2 = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "谢谢你！"}]},
        config=config,
        context=context,
    )
    
    assert response2 is not None
    structured2 = response2["structured_response"]
    assert isinstance(structured2, ResponseFormat)
    assert structured2.punny_response is not None
