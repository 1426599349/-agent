import requests
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

class CareerAgent:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        self.conversation_history = []
        self.user_profile = {}  # 仅记录用户主动提供的信息
        self.current_state = "general"
        print("Career Agent 初始化完成")
    
    def detect_state(self, user_input):
        """状态检测（不影响回答）"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["简历", "cv"]):
            self.current_state = "resume"
        elif any(word in user_input_lower for word in ["面试"]):
            self.current_state = "interview"
        elif any(word in user_input_lower for word in ["技能", "学习"]):
            self.current_state = "skills"
        else:
            self.current_state = "general"
    
    def update_profile_from_input(self, user_input):
        """仅当用户明显提供信息时才记录"""
        # 只有当用户明确提到个人信息时才记录
        if "我今年" in user_input or "我年龄" in user_input or "岁" in user_input:
            self.user_profile["age"] = user_input
        elif "我学" in user_input or "我毕业" in user_input or "学历" in user_input:
            self.user_profile["education"] = user_input
        elif "我工作" in user_input or "经验" in user_input or "从业" in user_input:
            self.user_profile["experience"] = user_input
        elif "我会" in user_input or "我熟悉" in user_input or "技能" in user_input:
            self.user_profile["skills"] = user_input
        # 不主动提取，只记录明确提供的信息
    
    def passive_chat(self, user_input):
        """被动模式对话 - 只回答问题，不询问信息"""
        
        # 检测状态（仅用于内部记录）
        self.detect_state(user_input)
        
        # 只有当用户明显提供信息时才记录
        self.update_profile_from_input(user_input)
        
        # 添加到记忆
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 保持记忆长度
        if len(self.conversation_history) > 8:
            self.conversation_history = self.conversation_history[-8:]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 被动模式提示词 - 明确禁止询问个人信息
        system_prompt = f"""你是一个职业规划助手。

重要原则：
1. 直接回答用户的问题，不要询问任何个人信息
2. 如果用户主动提供信息，可以基于这些信息给出更精准的建议
3. 如果信息不足，就给出通用性的专业建议
4. 绝对不要主动询问年龄、教育背景、工作经验等个人信息

用户主动提供的信息：{json.dumps(self.user_profile, ensure_ascii=False)}
当前对话主题：{self.current_state}

请基于以上原则提供专业建议。"""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # 添加对话历史
        for msg in self.conversation_history[-4:]:
            messages.append(msg)
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                response_content = result["choices"][0]["message"]["content"]
                self.conversation_history.append({"role": "assistant", "content": response_content})
                return response_content
            else:
                return f"API请求失败: {response.status_code}"
        except Exception as e:
            return f"发生异常: {e}"
    
    def show_status(self):
        """显示Agent状态"""
        print(f"\n=== Agent状态 ===")
        print(f"当前模式: {self.current_state}")
        print(f"用户主动提供的信息: {len(self.user_profile)} 项")
        for key, value in self.user_profile.items():
            print(f"  - {key}: {value}")
        print(f"对话记忆: {len(self.conversation_history)} 轮")
        print("================")

def main():
    """Agent版的主函数 - 保持与基础版相同的接口"""
    agent = CareerAgent()
    
    print("\n=== AI职业规划Agent ===")
    print("1. 开始职业咨询")
    print("2. 查看当前状态") 
    print("3. 返回主菜单")
    print("=" * 30)
    
    while True:
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            print("\n开始职业咨询（输入'退出'返回菜单）")
            while True:
                user_input = input("\n您: ").strip()
                if user_input.lower() in ['退出', 'exit', '返回']:
                    break
                elif user_input.lower() in ['状态', 'status']:
                    agent.show_status()
                    continue
                    
                response = agent.passive_chat(user_input)
                print(f"Agent: {response}")
                
        elif choice == "2":
            agent.show_status()
        elif choice == "3":
            print("返回主菜单...")
            break
        else:
            print("请输入有效选项 (1-3)")

if __name__ == "__main__":
    main()