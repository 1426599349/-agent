import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"

# 检查API密钥是否加载成功
if not DEEPSEEK_API_KEY:
    print("Warning: DEEPSEEK_API_KEY not found")
else:
    print("API Key loaded successfully")