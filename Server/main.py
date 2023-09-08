import pystray
import threading
from PIL import Image
from flask import Flask, request, jsonify
from plyer import notification
import atexit
import os

# 创建一个全局变量来存储消息
message = None

# 创建一个全局标志来控制线程是否运行
flask_thread_running = True

# 创建一个PyStray图标
def create_systray_icon():
    image = Image.open("icon.png")  # 你可以替换为自己的图标文件
    menu = (pystray.MenuItem('退出', exit_program),)
    icon = pystray.Icon("my_icon", image, "My App", menu=menu)
    icon.run()

# 退出程序
def exit_program(icon, item):
    global flask_thread_running
    flask_thread_running = False
    icon.stop()
    # 停止其他线程，如果有的话
    os._exit(0)  # 强制退出程序

# 创建Flask应用来接收HTTP消息
app = Flask(__name__)

@app.route('/api/message', methods=['POST'])
def receive_message():
    global message
    data = request.get_json()
    message = data.get('message')
    if message:
        notification.notify(
            title='新消息',
            message=message,
            app_name='My App'
        )
    return jsonify({'success': True})

# 启动Flask应用在一个独立的线程中
def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # 注册退出处理函数
    atexit.register(exit_program)

    # 创建并启动PyStray图标
    systray_thread = threading.Thread(target=create_systray_icon)
    systray_thread.start()

    # 启动Flask应用
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # 等待Flask应用线程结束
    flask_thread.join()
