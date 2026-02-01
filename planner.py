import dashscope
import json
import yaml

# Load config
cfg = yaml.safe_load(open("config.yaml"))

# Configure DashScope
dashscope.api_key = cfg["llm"]["api_key"]

def plan_action(goal, memory):
    prompt = f"""
你是一个自主的AI代理。
目标：
{goal}
记忆：
{memory}
请决定下一步要采取的行动。
用JSON格式回复：{{ "action": "post", "content": "..." }}
如果发现代码有潜在问题，action设为"post"并在content中详细说明问题。
如果代码没有问题，action设为"skip"。
"""
    
    response = dashscope.Generation.call(
        model=cfg["llm"]["model"],
        prompt=prompt,
        result_format='message'
    )
    
    if response.status_code == 200:
        content = response.output.choices[0].message.content
        print(content)
        return json.loads(content)
    else:
        raise Exception(f"DashScope API error: {response.message}")