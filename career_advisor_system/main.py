import requests
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

def test_api_connection():
    """原有的API测试功能"""
    print("正在测试API连接...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Hello, please reply with one sentence"}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        print(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("API Connection Success!")
            print("Model Reply:", result["choices"][0]["message"]["content"])
        else:
            print("API Request Failed")
            print("Error Details:", response.text)
    except Exception as e:
        print(f"Exception: {e}")

def run_basic_career_advisor():
    """运行基础版职业规划师"""
    try:
        from career_advisor import main as basic_main
        print("\n 启动基础版职业规划师...")
        basic_main()
    except ImportError:
        print(" 找不到 career_advisor.py")
    except Exception as e:
        print(f" 启动基础版时出错: {e}")

def run_agent_career_advisor():
    """运行Agent版职业规划师"""
    try:
        from career_agent import main as agent_main
        print("\n 启动Agent版职业规划师...")
        agent_main()
    except ImportError:
        print(" 找不到 career_agent.py，请先创建该文件")
    except Exception as e:
        print(f" 启动Agent版时出错: {e}")

def show_main_menu():
    """显示主菜单"""
    print("\n" + "="*50)
    print("我是你的职业规划师布雷，请问能有什么为您解答吗")
    print("="*50)
    print("1. 测试API连接")
    print("2. 基础版职业规划师")
    print("3. Agent版职业规划师（新增功能）")
    print("4. 退出系统")
    print("="*50)

def main():
    """主程序 - 在原有基础上扩展"""
    print("系统初始化完成！")
    
    while True:
        show_main_menu()
        choice = input("\n请选择功能 (1-4): ").strip()
        
        if choice == "1":
            test_api_connection()
        elif choice == "2":
            run_basic_career_advisor()
        elif choice == "3":
            run_agent_career_advisor()
        elif choice == "4":
            print("\n我是你的职业规划师布雷，请问能有什么为您解答吗！")
            break
        else:
            print(" 请输入有效选项 (1-4)")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()