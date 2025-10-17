# Chatbot Service

基于 LangChain v1 和 LangGraph v1 的初始化项目基座。

## 项目简介

这是一个智能网络受理助手的初始化项目，提供了基于 LangChain v1 框架的 AI Agent 基础架构。项目集成了 LangGraph 用于构建有状态的多步骤 AI 应用程序。

## 技术栈

- **LangChain**: v1.0.0+ (Alpha)
- **LangGraph**: v1.0.0+ (Alpha)
- **Python**: >=3.11
- **LLM 集成**: OpenAI, Qwen

## 主要特性

- ✅ AI Agent 创建与管理
- ✅ 工具（Tool）集成
- ✅ 运行时上下文支持
- ✅ 结构化输出
- ✅ 对话记忆管理
- ✅ LangGraph Studio 可视化支持

## 快速开始

### 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，添加必要的 API 密钥
```

### 运行示例

查看 `notebooks/langchain_v1_quickstart.ipynb` 获取快速入门示例。

## 项目结构

```
├── src/agent/          # Agent 核心代码
├── tests/              # 测试用例
├── notebooks/          # Jupyter 示例笔记本
├── langgraph.json      # LangGraph 配置
└── pyproject.toml      # 项目依赖配置
```

## 开发

```bash
# 代码检查
make lint

# 运行测试
make test
```

## License

MIT

