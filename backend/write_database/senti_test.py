import requests

API_URL = "http://api-cfk2z6ccq5m9r1k5.aistudio-app.com"

# 设置鉴权信息
headers = {
    # 请前往 https://aistudio.baidu.com/index/accessToken 查看 访问令牌 并替换
    "Authorization": "Bearer {b017e5e2d7c42a2a36d18d04491a76c4dafeb659}",
    "Content-Type": "application/json"

}
obj = {
    "text":"超级无敌开心"
}
# 调用
response = requests.get(API_URL, headers=headers, verify=False, params=obj)

# 打印接口返回
print(response.content)