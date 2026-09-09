# 个人AI记忆服务 (Personal Memory Service)

一个基于MCP协议的个人AI记忆服务，为各种AI客户端提供长期记忆能力。

## 核心特性

### 🧠 事实存储
- 存储带上下文的事实，而非结论
- 支持场景标签、来源追踪、重要性分级
- 自动时间戳和访问统计

### 🔍 语义搜索
- 基于ChromaDB的向量语义搜索
- 支持场景过滤和相似度排序
- 实时更新访问记录

### 🌡️ 智能分层
- 热层：活跃记忆，快速检索
- 温层：中等活跃度记忆
- 冷层：归档记忆，按需检索

### 🔌 MCP协议支持
- 标准MCP工具接口
- 支持多种AI客户端连接
- 易于集成和扩展

## 快速开始

### 前置要求
- Python 3.10+
- 支持MCP的AI客户端（如Claude Desktop）

### 方式一：本地运行（推荐）

#### 1. 克隆项目
```bash
git clone https://github.com/sjcxxx-afk/personal-memory.git
cd personal-memory
```

#### 2. 安装依赖
```bash
# 安装核心依赖（不包含ChromaDB）
pip install mcp pydantic

# 或者安装完整依赖（包含ChromaDB，需要更多时间）
pip install -r requirements.txt
```

#### 3. 运行服务器
```bash
# 直接运行
python run_server.py

# 或者使用模块方式运行
python -m src.server
```

#### 4. 配置AI客户端

##### Claude Desktop配置
在Claude Desktop配置文件中添加：
```json
{
  "mcpServers": {
    "personal-memory": {
      "command": "python",
      "args": ["run_server.py"],
      "env": {
        "PYTHONPATH": "D:\\个人项目\\个人知识库\\personal-memory"
      }
    }
  }
}
```

### 方式二：Docker运行

#### 1. 构建并启动服务
```bash
# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 2. 配置AI客户端

##### Claude Desktop配置
在Claude Desktop配置文件中添加：
```json
{
  "mcpServers": {
    "personal-memory": {
      "command": "docker",
      "args": ["exec", "-i", "personal-memory-service", "python", "-m", "src.server"],
      "env": {}
    }
  }
}
```

## MCP工具

### 1. store_fact - 存储事实
```json
{
  "content": "用户对花生过敏",
  "scene": "health",
  "source": "chat_2026-09-07",
  "importance": "high"
}
```

### 2. search_facts - 搜索事实
```json
{
  "query": "过敏信息",
  "scene_filter": "health",
  "limit": 5
}
```

### 3. list_facts - 列出事实
```json
{
  "scene_filter": "work",
  "limit": 10
}
```

### 4. get_fact_details - 获取事实详情
```json
{
  "fact_id": "fact-uuid-here"
}
```

### 5. get_memory_stats - 获取统计信息
```json
{}
```

## 项目结构
```
personal-memory/
├── src/                    # 源代码
│   ├── server.py          # MCP服务器主入口
│   ├── models.py          # 数据模型定义
│   ├── storage/           # 存储层
│   │   ├── fact_store.py  # SQLite存储
│   │   └── vector_store.py # ChromaDB向量存储
│   ├── tools/             # MCP工具实现
│   │   ├── store_tool.py  # 存储工具
│   │   └── search_tool.py # 搜索工具
│   └── utils/             # 工具函数
├── data/                  # 数据目录
│   ├── facts/            # 冷存储
│   └── chroma/           # ChromaDB数据
├── config/               # 配置文件
├── Dockerfile            # Docker配置
├── docker-compose.yml    # Docker Compose配置
└── requirements.txt      # Python依赖
```

## 配置说明

### 环境变量
- `LOG_LEVEL`: 日志级别（DEBUG, INFO, WARNING, ERROR）
- `PYTHONPATH`: Python路径

### 存储配置
- SQLite数据库：`data/memory.db`
- ChromaDB数据：`data/chroma/`
- 冷存储目录：`data/facts/`

## 开发指南

### 本地开发
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行服务器
python -m src.server
```

### 测试
```bash
# 运行测试
pytest tests/

# 测试MCP工具
python -c "
import asyncio
from src.tools.store_tool import StoreTool
from src.tools.search_tool import SearchTool

async def test():
    store = StoreTool()
    search = SearchTool()
    
    # 测试存储
    result = await store.store_fact('测试事实', 'test', 'test', 'medium')
    print('存储结果:', result)
    
    # 测试搜索
    result = await search.search_facts('测试', limit=3)
    print('搜索结果:', result)

asyncio.run(test())
"
```

## 故障排除

### 常见问题

#### 1. ChromaDB初始化失败
```
错误: Error initializing ChromaDB
解决: 检查data/chroma目录权限，确保可写
```

#### 2. MCP连接失败
```
错误: MCP server connection failed
解决: 检查Docker容器是否运行，端口是否正确
```

#### 3. 依赖安装失败
```
错误: pip install failed
解决: 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 下一步计划

### 第二阶段功能
- [ ] 使用驱动的冷热分层
- [ ] 记忆点索引系统
- [ ] 配置界面（CLI/Web）
- [ ] 隐私控制

### 第三阶段功能
- [ ] 多客户端并发支持
- [ ] 高级安全特性
- [ ] 性能优化
- [ ] 社区插件生态

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发规范
- 代码风格：遵循PEP 8
- 提交信息：使用中文，格式为 `类型: 描述`
- 测试：新功能需要添加测试

## 许可证

MIT License

## 致谢

- [MCP协议](https://modelcontextprotocol.io/)
- [ChromaDB](https://www.trychroma.com/)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)