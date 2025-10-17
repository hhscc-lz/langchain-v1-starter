# Project Memory

## HumanInTheLoopMiddleware 使用指南

### 配置

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents.middleware.human_in_the_loop import ToolConfig

HumanInTheLoopMiddleware(
    interrupt_on={
        "tool_name": True,  # 允许所有操作
        "tool2": ToolConfig(
            allow_accept=True,    # 直接批准
            allow_edit=True,      # 修改后执行
            allow_respond=True,   # 拒绝并反馈
            description="描述"
        ),
        "auto_tool": False,  # 不拦截
    }
)
```

### Resume 格式

```python
# Accept
Command(resume=[{"type": "accept"}])

# Edit
Command(resume=[{
    "type": "edit",
    "args": {"action": "tool_name", "args": {"param": "value"}}
}])

# Response
Command(resume=[{"type": "response", "args": "拒绝原因"}])
```

### LangGraph Dev 输入

```json
[{"type": "accept"}]
```

**重要**:
- 必须是数组 `[...]`
- 响应数量 = 拦截的工具调用数量
- 多个工具时: `[{"type": "accept"}, {"type": "accept"}]`

### 三种决策

| 类型 | 效果 |
|------|------|
| accept | 直接执行原始调用 |
| edit | 修改参数后执行 |
| response | 拒绝，AI 收到反馈后重新规划 |
