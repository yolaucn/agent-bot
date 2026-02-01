import time
import yaml
from identity import GitHubAgentIdentity, get_github_token
from memory import load_memory, save_memory
from planner import plan_action
from actions import post_to_github

# 加载配置
cfg = yaml.safe_load(open("config.yaml"))

# 初始化身份管理 - 支持两种方式
def get_auth_token():
    """获取GitHub认证token，支持两种方式"""
    if "app_id" in cfg["github"] and cfg["github"]["app_id"]:
        # 方式2: GitHub App
        print("🔐 使用GitHub App认证...")
        identity_manager = GitHubAgentIdentity(
            app_id=cfg["github"]["app_id"],
            installation_id=cfg["github"]["installation_id"],
            private_key_path=cfg["github"]["private_key_path"]
        )
        return identity_manager.get_token()
    else:
        # 方式1: Personal Access Token
        print("🔐 使用Personal Access Token认证...")
        return get_github_token(cfg)

# 载入记忆
memory = load_memory()

# 模拟 commit 事件列表
simulated_commits = [
    {"file": "calculator.py", "diff": "def divide(a, b): return a / b"},
    {"file": "math_utils.py", "diff": "def add(a, b): return a + b"}
]

print("🤖 AI Agent 启动 - 自主代码审查模式")
print("=" * 50)

# 轮询循环 - 只运行一次用于测试
print("\n🔍 检测新提交...")
for commit in simulated_commits:
    print(f"\n📁 正在分析提交: {commit['file']}")
    
    # AI决策：分析 diff 是否有 bug
    try:
        print("🧠 AI正在思考...")
        decision = plan_action(
            goal=f"检测以下代码差异中的潜在bug，如果有问题请建议创建issue：\n{commit['diff']}",
            memory=memory
        )
        print(f"💭 AI决策结果: {decision}")
    except Exception as e:
        print(f"❌ AI决策过程出错: {e}")
        continue
    
    # 自主行动：发 Issue
    if decision.get("action") == "post":
        try:
            print("🚀 AI决定自主发帖...")
            token = get_auth_token()
            result = post_to_github(
                token,
                cfg["github"]["repo"],
                title=f"🐛 {commit['file']} 中发现潜在问题",
                content=decision.get("content", "")
            )
            memory["posts"].append(result)
            print(f"✅ AI自主创建Issue成功: #{result['post_id']}")
            print(f"📝 Issue标题: {result['title']}")
        except Exception as e:
            print(f"❌ 创建Issue时出错: {e}")
    else:
        print(f"✅ AI判断 {commit['file']} 无需创建Issue")

# 保存 Memory
save_memory(memory)
print("\n🎉 AI Agent自主分析完成！")
print("📊 本次运行统计:")
print(f"   - 分析文件数: {len(simulated_commits)}")
print(f"   - 创建Issue数: {len([p for p in memory.get('posts', []) if 'post_id' in p])}")
print("   - AI完全自主运行，无需人工干预")