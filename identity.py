import os
import yaml
import jwt
import time
import requests

class GitHubAgentIdentity:
    def __init__(self, app_id, installation_id, private_key_path):
        self.app_id = app_id
        self.installation_id = installation_id
        self.private_key_path = private_key_path
        self._cached_token = None
        self._token_expires_at = 0
    
    def _generate_jwt(self):
        """生成 JWT token"""
        with open(self.private_key_path, "r") as f:
            private_key = f.read()
        
        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + (10 * 60),  # 10 分钟过期
            "iss": self.app_id
        }
        
        return jwt.encode(payload, private_key, algorithm="RS256")
    
    def get_token(self):
        """获取 GitHub Installation Token"""
        # 如果缓存的 token 还没过期，直接返回
        if self._cached_token and time.time() < self._token_expires_at:
            return self._cached_token
        
        # 生成新的 token
        jwt_token = self._generate_jwt()
        
        url = f"https://api.github.com/app/installations/{self.installation_id}/access_tokens"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json"
        }
        
        response = requests.post(url, headers=headers)
        
        if response.status_code == 201:
            token_data = response.json()
            self._cached_token = token_data["token"]
            # 设置过期时间（提前 5 分钟刷新）
            expires_at = time.strptime(token_data["expires_at"], "%Y-%m-%dT%H:%M:%SZ")
            self._token_expires_at = time.mktime(expires_at) - 300
            return self._cached_token
        else:
            raise Exception(f"Failed to get installation token: {response.status_code} - {response.text}")

def get_github_token(cfg):
    """获取GitHub Personal Access Token"""
    token = cfg["github"].get("token")
    if not token:
        raise ValueError("GitHub token not found in config")
    return token

def verify_agent():
    """向后兼容的函数"""
    cfg = yaml.safe_load(open('config.yaml'))
    token = cfg['github']['token']
    if not token:
        raise ValueError('GITHUB_TOKEN not found in config')
    return {
        "agent_id": "github_agent_001",
        "verified": True,
        "token": token
    }