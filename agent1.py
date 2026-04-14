print("111")
APIkey = "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"
AGENT_SYSTEM_PROMPT = """
你是一个智能旅行助手。你的任务是分析用户的请求,并使用可用工具一步步地解决问题。
# 可用工具:
- `get_weather(city: str)`: 查询指定城市的实时天气。- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。
# 输出格式要求:
你的每次回复必须严格遵循以下格式,包含一对Thought和Action:
Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]
Action的格式必须是以下之一:
1. 调用工具:function_name(arg_name="arg_value")
2. 结束任务:Finish[最终答案]
# 重要提示:
- 每次只输出一对Thought-Action
- Action必须在同一行,不要换行
- 当收集到足够信息可以回答用户问题时,必须使用 Action: Finish[最终答案] 格式结束
"""
import requests

#工具1查询真实天气
def get_weather(city:str) -> str:
    """
    通过调用wttr.in API查询真实天气
    """
    url = f"https://wttr.in/{city}?format=j1"
    """
    这是一个本地查询天气的基于终端的天气预报服务
    https://wttr.in 查询本地天气，可以在浏览器打开查看
    """
    try:
        #第一步发起网络请求，调用天气查询，response得到json输出
        response = requests.get(url)
        # 检查响应状态码是否为200 (成功)
        response.raise_for_status()
        # 解析返回的JSON数据
        data = response.json()
        # 提取当前天气状况 看样子天气在json数据中的存贮格式为列表形式
        current_condition = data['current_condition'][0]
        weather_desc = current_condition['weatherDesc'][0]['value']
        temp_c = current_condition['temp_C']
         # 格式化成自然语言返回（f-string（格式化字符串字面值）语法）
        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"
    except requests.exceptions.RequestException as e:
        # 处理一场请求错误
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError) as e:
        # 处理数据解析错误
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"

