import woodAI
import os
os.environ['WOODAI_RUNTIME_ENV'] = 'test'
os.environ['WOODAI_USER_AUTH'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDb2RlbWFvIEF1dGgiLCJ1c2VyX3R5cGUiOiJzdHVkZW50IiwiZGV2aWNlX2lkIjowLCJ1c2VyX2lkIjoxMDAwNzEwNDgyLCJpc3MiOiJBdXRoIFNlcnZpY2UiLCJwaWQiOiIyM0FWWGFsbyIsImV4cCI6MTcxOTEyOTk1NywiaWF0IjoxNzE1MjQxOTU3LCJqdGkiOiI2ZDhiM2ZjOS0zZDRjLTQ2ZGEtYmM2NS02MzU1NjUyMTdkN2EifQ.gujRokpg7pRhnjqnHrYKcz0mdnZox-ClXjFU-3XzVAk'

# 2. 系统设置: 机器人角色，上下文记录
woodAI.chat_set("你是一个相声演员", 5)

# 3. 进入对话:
for i in range(3):
    prompt = input("Uesr: ")
    print("ChatBot: ", end="")
    answer = woodAI.chat(prompt, True)
    # print(f"ChatBot:{answer}")

# 4. 清空上下文关联记录
woodAI.chat_clear()
