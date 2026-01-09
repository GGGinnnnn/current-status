import time
import threading
import requests
import win32gui
import pystray
from pystray import MenuItem as item
from PIL import Image
import tkinter as tk

SERVER_URL = "https://curly-scene-7514.1504188084.workers.dev/update"


manual_status = None
running = True

# ======================
# 获取前台应用
# ======================
def get_foreground_app():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return title if title else "未知应用"

def get_status():
    if manual_status == "busy":
        return "在忙"
    if manual_status == "sleep":
        return "在睡觉"
    return get_foreground_app()

# ======================
# 状态发送线程
# ======================
def sender_loop():
    while running:
        try:
            requests.post(SERVER_URL, json={"status": get_status()}, timeout=3)
        except:
            pass
        time.sleep(5)

# ======================
# 托盘菜单回调
# ======================
def set_auto(icon, item):
    global manual_status
    manual_status = None

def set_busy(icon, item):
    global manual_status
    manual_status = "busy"

def set_sleep(icon, item):
    global manual_status
    manual_status = "sleep"

def quit_app(icon, item):
    global running
    running = False
    icon.stop()

# ======================
# GUI 面板
# ======================
def show_panel(icon, item):
    root = tk.Tk()
    root.title("状态设置")
    root.geometry("200x150")

    tk.Button(root, text="自动", command=lambda: set_auto(None, None)).pack(fill="x")
    tk.Button(root, text="在忙", command=lambda: set_busy(None, None)).pack(fill="x")
    tk.Button(root, text="在睡觉", command=lambda: set_sleep(None, None)).pack(fill="x")

    root.mainloop()

# ======================
# 主程序
# ======================
def main():
    threading.Thread(target=sender_loop, daemon=True).start()

    image = Image.open("icon.ico")  # 你的图标
    menu = (
        item("打开面板", show_panel),
        item("自动", set_auto),
        item("在忙", set_busy),
        item("在睡觉", set_sleep),
        item("退出", quit_app)
    )

    tray = pystray.Icon("status", image, "电脑状态", menu)
    tray.run()

main()
