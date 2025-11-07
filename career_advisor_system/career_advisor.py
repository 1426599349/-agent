import requests
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

class CareerAdvisor:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
    
    def call_deepseek(self, prompt):
        """调用DeepSeek API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "你是一名资深职业规划师，拥有20年人力资源和职业发展咨询经验。请提供专业、具体、可执行的建议。"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"API请求失败: {response.text}"
        except Exception as e:
            return f"发生异常: {e}"
    
    def analyze_career_profile(self, user_info):
        """分析职业画像"""
        prompt = f"""
请基于以下用户信息进行职业画像分析，并按照以下格式输出：

职业画像分析

核心优势
- 优势1
- 优势2

技能评估
- 已具备技能
- 待提升技能

职业建议
- 推荐职业方向1
- 推荐职业方向2

发展建议
- 短期行动建议
- 长期规划建议

用户信息：
{user_info}
"""
        return self.call_deepseek(prompt)
    
    def optimize_resume(self, resume, job_description):
        """优化简历"""
        prompt = f"""
作为职业规划师，请分析以下简历与目标职位的匹配度，并提供优化建议：

简历优化建议

匹配度分析
- 优势匹配点
- 差距分析

关键词建议
- 需要添加的关键词
- 需要强化的关键词

内容优化
- 经历描述优化建议
- 技能展示优化建议

简历内容：
{resume}

目标职位描述：
{job_description}
"""
        return self.call_deepseek(prompt)
    
    def interview_coaching(self, job_position):
        """面试指导"""
        prompt = f"""
为以下职位提供面试指导：

面试准备指南

可能的问题
- 技术问题
- 行为面试问题

回答策略
- 回答框架
- 注意事项

提问建议
- 向面试官提问的建议

目标职位：{job_position}
"""
        return self.call_deepseek(prompt)

def main():
    advisor = CareerAdvisor()
    
    print("=== AI职业规划师系统 ===")
    print("1. 职业画像分析")
    print("2. 简历优化建议")
    print("3. 面试指导")
    print("4. 退出")
    
    while True:
        choice = input("\n请选择功能 (1-4): ")
        
        if choice == "1":
            print("\n--- 职业画像分析 ---")
            age = input("年龄: ")
            education = input("教育背景: ")
            experience = input("工作经历: ")
            skills = input("技能专长: ")
            goals = input("职业目标: ")
            
            user_info = f"""
年龄: {age}
教育背景: {education}
工作经历: {experience}
技能专长: {skills}
职业目标: {goals}
"""
            result = advisor.analyze_career_profile(user_info)
            print(f"\n分析结果:\n{result}")
            
        elif choice == "2":
            print("\n--- 简历优化 ---")
            resume = input("请粘贴你的简历内容: ")
            jd = input("请粘贴目标职位描述: ")
            
            result = advisor.optimize_resume(resume, jd)
            print(f"\n优化建议:\n{result}")
            
        elif choice == "3":
            print("\n--- 面试指导 ---")
            position = input("目标职位: ")
            
            result = advisor.interview_coaching(position)
            print(f"\n面试指导:\n{result}")
            
        elif choice == "4":
            print("感谢使用AI职业规划师！")
            break
        else:
            print("请输入有效选项 (1-4)")

if __name__ == "__main__":
    main()