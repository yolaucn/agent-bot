# 设置指南

## 前置要求

- Python 3.8+
- GitHub 账号
- 阿里云账号（用于百炼服务）

## 详细设置步骤

### 1. 克隆项目

```bash
git clone https://github.com/your_username/agent-bot.git
cd agent-bot
```

### 2. 安装依赖

使用 uv (推荐):
```bash
uv sync
```

或使用 pip:
```bash
pip install -r requirements.txt
```

### 3. 配置 GitHub 认证

#### 选项A: Personal Access Token (简单)

1. 访问 GitHub Settings > Developer settings > Personal access tokens
2. 点击 "Generate new token (classic)"
3. 选择以下权限：
   - `repo` (完整仓库访问权限)
   - `issues` (读写 issues)
4. 复制生成的 token

#### 选项B: GitHub App (推荐，更安全)

1. 访问 GitHub Settings > Developer settings > GitHub Apps
2. 点击 "New GitHub App"
3. 填写基本信息：
   - App name: 你的应用名称
   - Homepage URL: 你的项目URL
   - Webhook URL: 可以暂时填写 `https://example.com`
4. 设置权限：
   - Repository permissions:
     - Issues: Read & write
     - Metadata: Read
     - Contents: Read (如果需要读取代码)
5. 创建后，记录 App ID
6. 生成并下载私钥文件 (.pem)
7. 安装 App 到你的仓库
8. 记录 Installation ID (在安装页面的URL中)

### 4. 配置阿里百炼

1. 注册阿里云账号：https://www.aliyun.com/
2. 开通百炼服务：https://dashscope.aliyun.com/
3. 创建 API Key：
   - 访问控制台
   - 点击 "创建 API Key"
   - 复制生成的 API Key

### 5. 创建配置文件

复制示例配置文件：
```bash
cp config.example.yaml config.yaml
```

编辑 `config.yaml`：

```yaml
agent:
  name: github_agent_001
  goal: "检测代码提交中的潜在bug并自动创建GitHub Issue"

github:
  # 如果使用 Personal Access Token
  token: "ghp_your_actual_token_here"
  repo: "your_username/your_repo_name"
  
  # 如果使用 GitHub App
  app_id: "your_app_id"
  installation_id: "your_installation_id"
  private_key_path: "path/to/your-private-key.pem"

llm:
  provider: dashscope
  model: qwen-turbo
  api_key: "sk-your_actual_api_key_here"
```

### 6. 测试配置

运行测试：
```bash
uv run main.py
```

如果配置正确，你应该看到类似输出：
```
=== 检测新提交 ===
正在分析提交: calculator.py
决策结果: {...}
已创建Issue: {...}
分析完成！
```

## 故障排除

### GitHub 认证问题

- 确保 token 有正确的权限
- 检查仓库名称格式：`username/repository`
- 如果使用 GitHub App，确保已正确安装到目标仓库

### 阿里百炼 API 问题

- 确保 API Key 正确
- 检查账户余额
- 确认已开通百炼服务

### 其他问题

- 检查网络连接
- 确认 Python 版本 >= 3.8
- 查看错误日志获取详细信息

## 安全建议

- 不要将 `config.yaml` 提交到版本控制
- 定期轮换 API 密钥
- 使用 GitHub App 而不是 Personal Access Token
- 限制 token 权限到最小必要范围