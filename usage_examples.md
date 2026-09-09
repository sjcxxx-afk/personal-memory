# 个人AI记忆服务 - 使用示例

## 基本使用流程

### 1. 启动服务

```powershell
# 进入项目目录
cd personal-memory

# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 2. 配置AI客户端

将以下配置添加到Claude Desktop的配置文件中：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

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

### 3. 与AI对话示例

#### 存储事实

**用户**: 请记住，我对花生过敏，需要避免所有花生制品。

**AI**: 我来帮你记住这个重要的健康信息。
*(AI调用store_fact工具)*

```
✅ Fact stored successfully!

ID: 550e8400-e29b-41d4-a716-446655440000
Content: 用户对花生过敏，需要避免所有花生制品
Scene: health
Source: chat
Importance: high
Timestamp: 2026-09-08T10:30:00
```

#### 存储偏好

**用户**: 我写PPT时喜欢简洁的风格，不要太多文字。

**AI**: 我记下你的PPT风格偏好了。
*(AI调用store_fact工具)*

```
✅ Fact stored successfully!

ID: 550e8400-e29b-41d4-a716-446655440001
Content: 用户写PPT时喜欢简洁风格，不要太多文字
Scene: work
Source: chat
Importance: medium
Timestamp: 2026-09-08T10:35:00
```

#### 搜索记忆

**用户**: 我有什么饮食限制吗？

**AI**: 让我查一下你的健康记录。
*(AI调用search_facts工具)*

```
🔍 Found 1 fact(s) matching: '饮食限制' in scene 'health':

1. [health] 用户对花生过敏，需要避免所有花生制品
   Similarity: 0.92
   ID: 550e8400-e29b-41d4-a716-446655440000
   Source: chat | Importance: high
   Temperature: hot | Accessed: 1 times
```

**AI**: 根据记录，你对花生过敏，需要避免所有花生制品。需要我帮你找一些不含花生的餐厅推荐吗？

#### 列出所有记忆

**用户**: 列出你记住的所有事情。

**AI**: 我来列出所有存储的记忆。
*(AI调用list_facts工具)*

```
📋 Found 2 fact(s):

1. [health] 用户对花生过敏，需要避免所有花生制品
   ID: 550e8400-e29b-41d4-a716-446655440000
   Source: chat | Importance: high
   Temperature: hot | Accessed: 1 times
   Stored: 2026-09-08 10:30

2. [work] 用户写PPT时喜欢简洁风格，不要太多文字
   ID: 550e8400-e29b-41d4-a716-446655440001
   Source: chat | Importance: medium
   Temperature: hot | Accessed: 0 times
   Stored: 2026-09-08 10:35
```

## 高级使用场景

### 场景1: 工作项目记忆

```
用户: 记住，我在做Q3财报分析项目，截止日期是9月30日。

AI: 我记下你的项目信息了。
[存储为work场景，high重要性]

--- 一周后 ---

用户: 我最近在忙什么项目？

AI: 让我查一下你的工作记录。
[搜索work场景的事实]

根据记录，你正在做Q3财报分析项目，截止日期是9月30日。
还有22天，进展如何？需要我帮你整理相关资料吗？
```

### 场景2: 学习笔记记忆

```
用户: 今天学了Python的装饰器，核心概念是闭包和高阶函数。

AI: 我记下你的学习内容了。
[存储为education场景]

--- 几天后 ---

用户: 我之前学过什么Python知识？

AI: 让我查一下你的学习记录。
[搜索education场景中关于Python的事实]

你之前学习过Python装饰器，核心概念是闭包和高阶函数。
需要我帮你复习或者深入学习相关主题吗？
```

### 场景3: 生活习惯记忆

```
用户: 我每天早上7点起床，晚上11点睡觉。

AI: 我记下你的作息习惯了。
[存储为life场景]

用户: 我喜欢喝美式咖啡，不加糖不加奶。

AI: 我记下你的咖啡偏好了。
[存储为life场景]

--- 需要推荐时 ---

用户: 帮我推荐一个咖啡店。

AI: 根据你的偏好，你喜欢美式咖啡，不加糖不加奶。
让我帮你找一家美式咖啡做得好的店...
```

## MCP工具详细参数

### store_fact

```json
{
  "content": "事实内容（必填）",
  "scene": "场景标签（可选，默认general）",
  "source": "来源（可选，默认chat）",
  "importance": "重要性（可选，默认medium）"
}
```

**场景标签建议**:
- `work` - 工作相关
- `life` - 生活习惯
- `health` - 健康信息
- `finance` - 财务信息
- `education` - 学习教育
- `entertainment` - 娱乐爱好
- `social` - 社交关系
- `travel` - 旅行相关
- `food` - 饮食偏好
- `general` - 通用/其他

**重要性级别**:
- `high` - 高（健康、安全等关键信息）
- `medium` - 中（一般偏好、习惯）
- `low` - 低（临时信息、可遗忘）

### search_facts

```json
{
  "query": "搜索关键词（必填）",
  "scene_filter": "场景过滤（可选）",
  "limit": "返回数量（可选，默认5）"
}
```

### list_facts

```json
{
  "scene_filter": "场景过滤（可选）",
  "limit": "返回数量（可选，默认10）"
}
```

### get_fact_details

```json
{
  "fact_id": "事实ID（必填）"
}
```

### get_memory_stats

```json
{}
```

## 最佳实践

### 1. 存储事实时

- ✅ 存储具体的事实，而非结论
  - 好: "2026年9月，用户在准备Q3财报时要求简洁风格"
  - 差: "用户喜欢简洁风格"

- ✅ 包含上下文信息
  - 好: "用户对花生过敏，因为花生会导致严重过敏反应"
  - 差: "用户对花生过敏"

- ✅ 使用合适的场景标签
  - 健康信息 → `health`
  - 工作偏好 → `work`
  - 生活习惯 → `life`

### 2. 搜索记忆时

- 使用自然语言描述你要找的信息
- 可以指定场景过滤，提高搜索精度
- 如果结果不理想，尝试换个关键词

### 3. 管理记忆

- 定期使用 `get_memory_stats` 查看记忆统计
- 重要信息设置为 `high` 重要性
- 临时信息可以设置为 `low` 重要性

## 故障排除

### 问题: AI说无法连接到记忆服务

**解决方案**:
1. 检查Docker容器是否运行: `docker-compose ps`
2. 查看容器日志: `docker-compose logs -f`
3. 重启服务: `docker-compose restart`

### 问题: 搜索结果不准确

**解决方案**:
1. 尝试不同的关键词
2. 使用场景过滤缩小范围
3. 检查存储的事实是否包含足够上下文

### 问题: 服务响应慢

**解决方案**:
1. 检查Docker资源限制
2. 减少返回结果数量 (limit参数)
3. 使用场景过滤减少搜索范围

## 下一步

完成第一阶段后，我们将继续开发：

- [ ] 冷热分层机制
- [ ] 记忆点索引系统
- [ ] 配置界面
- [ ] 隐私控制

敬请期待！