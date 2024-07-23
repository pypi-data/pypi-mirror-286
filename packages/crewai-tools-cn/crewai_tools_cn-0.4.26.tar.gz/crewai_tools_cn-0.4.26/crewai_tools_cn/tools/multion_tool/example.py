import os

from crewai import Agent, Crew, Task
from multion_tool import MultiOnTool

os.environ["OPENAI_API_KEY"] = "你的密钥"

multion_browse_tool = MultiOnTool(api_key="你的密钥")

# 创建一个新的代理
Browser = Agent(
    role="浏览器代理",
    goal="使用自然语言控制网络浏览器",
    backstory="一个专业的浏览代理。",
    tools=[multion_browse_tool],
    verbose=True,
)

# 定义任务
browse = Task(
    description="总结排名前 3 的热门 AI 新闻标题",
    expected_output="排名前 3 的热门 AI 新闻标题的摘要",
    agent=Browser,
)


crew = Crew(agents=[Browser], tasks=[browse])

crew.kickoff()
