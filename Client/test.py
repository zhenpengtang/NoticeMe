import requests
import json

# 发送消息到你的程序
def send_message(message):
    url = 'http://localhost:5000/api/message'
    data = {'message': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 200:
        print(f"消息发送成功: {message}")
    else:
        print(f"消息发送失败: {message}")

if __name__ == '__main__':
    while True:
        message = input("请输入要发送的消息（输入 '退出' 来退出测试）: ")
        if message == '退出':
            break
        send_message(message)
