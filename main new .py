import subprocess
import re
import time
import tkinter as tk
from tkinter import messagebox
import threading

restart_time = 9600  # 1小时

initial_ip = '192.168.8.180'
initial_username = 'albert'
initial_password = 'admin'
initial_ipmitool_path = r'C:\Users\n666c\ipmitool.exe'
ipmitool_path = initial_ipmitool_path

def update_info():
    global ipmitool_path
    new_ip = ip_entry.get()
    new_username = username_entry.get()
    new_password = password_entry.get()
    messagebox.showinfo("更新信息", f"IP: {new_ip}\n用户名: {new_username}\n密码: {new_password}")

def update_ipmitool_path():
    global ipmitool_path
    ipmitool_path = ipmitool_path_entry.get()
    messagebox.showinfo("更新IPMITOOL路径", f"新的IPMITOOL路径: {ipmitool_path}")

root = tk.Tk()
root.title("IPMI信息更新  此程序由贺某人制作，qq3342196810")

# IP、用户名、密码及路径输入框
ip_label = tk.Label(root, text="IP:")
ip_label.pack(pady=(10, 0))
ip_entry = tk.Entry(root, width=20, textvariable=tk.StringVar(value=initial_ip))
ip_entry.pack()

username_label = tk.Label(root, text="用户名:")
username_label.pack(pady=(10, 0))
username_entry = tk.Entry(root, width=20, textvariable=tk.StringVar(value=initial_username))
username_entry.pack()

password_label = tk.Label(root, text="密码:")
password_label.pack(pady=(10, 0))
password_entry = tk.Entry(root, width=20, show="*", textvariable=tk.StringVar(value=initial_password))
password_entry.pack()

update_button = tk.Button(root, text="更新信息,更新完成后请关闭此配置页面", command=update_info)
update_button.pack(pady=(20, 10))

ipmitool_path_label = tk.Label(root, text="IPMITOOL路径:")
ipmitool_path_label.pack(pady=(10, 0))
ipmitool_path_entry = tk.Entry(root, width=50, textvariable=tk.StringVar(value=initial_ipmitool_path))
ipmitool_path_entry.pack()

update_ipmitool_button = tk.Button(root, text="更新IPMITOOL路径", command=update_ipmitool_path)
update_ipmitool_button.pack(pady=(10, 10))

def run_ipmitool_command(ip, username, password, command):
    cmd = [ipmitool_path, '-I', 'lanplus', '-H', ip, '-U', username, '-P', password] + command.split()
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode} and output:")
        print(e.stderr)
        return None

def get_cpu_temp(ip, username, password):
    output = run_ipmitool_command(ip, username, password, 'sensor')
    if output:
        match = re.search(r'CPU1_Temp\s+\|\s+([\d.]+)\s+\|\s+degrees C', output, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None

def set_fan_speed(ip, username, password, speed):
    cmd = ['raw', '0x2e', '0x30', '00', '00', f'{speed:02x}']
    subprocess.run([ipmitool_path, '-I', 'lanplus', '-H', ip, '-U', username, '-P', password] + cmd, check=True)

def main():
    ip = ip_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    temp = get_cpu_temp(ip, username, password)
    if temp is not None:
        print(f"CPU Temperature: {temp}°C")

        if temp <= 39:
            set_fan_speed(ip, username, password, 20)
            print("success20")
        elif temp <= 49:
            set_fan_speed(ip, username, password, 24)
            print("success24")
        elif temp <= 58:
            set_fan_speed(ip, username, password, 40)
            print("success40")
        elif temp <= 68:
            set_fan_speed(ip, username, password, 60)
            print("success60")
        elif temp <= 78:
            set_fan_speed(ip, username, password, 80)
            print("success70")
        elif temp > 88:
            set_fan_speed(ip, username, password, 100)
            print("success100")

    print(time.localtime(time.time()))

def background_task():
    while True:
        main()
        time.sleep(100)

thread = threading.Thread(target=background_task, daemon=True)
thread.start()

root.mainloop()
