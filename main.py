import subprocess
import re
import time
import tkinter as tk
from tkinter import messagebox


restart_time = 9600  # 1小时

# 假设这是初始的IP、用户名和密码
initial_ip = '192.168.8.180'
initial_username = 'albert'
initial_password = 'admin'
initial_ipmitool_path = r'C:\Users\n666c\ipmitool.exe'
# 全局变量来存储ipmitool路径（虽然在实际应用中，最好使用配置文件）
ipmitool_path = initial_ipmitool_path
def update_info():
    # 从GUI获取新的IP、用户名和密码
    new_ip = ip_entry.get()
    new_username = username_entry.get()
    new_password = password_entry.get()

    # 这里可以添加代码来验证输入或执行其他操作
    # 例如，检查IP地址格式、用户名和密码的长度等

    # 显示更新后的信息（可选）
    messagebox.showinfo("更新信息", f"IP: {new_ip}\n用户名: {new_username}\n密码: {new_password}")

    # 在实际应用中，您可能希望将这些信息保存到文件、数据库或用于其他目的


# 创建主窗口
root = tk.Tk()
root.title("IPMI信息更新  此程序由贺某人制作，qq3342196810")

# 创建标签和条目控件
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

# 创建更新按钮
update_button = tk.Button(root, text="更新信息,更新完成后请关闭此配置页面", command=update_info)
update_button.pack(pady=(20, 10))


def update_ipmitool_path():
    # 从GUI获取新的ipmitool路径
    global ipmitool_path  # 声明为全局变量以在函数内部修改
    new_path = ipmitool_path_entry.get()

    # 这里可以添加代码来验证路径是否存在或可执行等

    # 更新全局变量
    ipmitool_path = new_path

    # 显示更新后的路径（可选）
    messagebox.showinfo("更新IPMITOOL路径", f"新的IPMITOOL路径: {ipmitool_path}")


# 添加ipmitool路径的标签和条目控件
ipmitool_path_label = tk.Label(root, text="IPMITOOL路径:")
ipmitool_path_label.pack(pady=(10, 0))
ipmitool_path_entry = tk.Entry(root, width=50, textvariable=tk.StringVar(value=initial_ipmitool_path))
ipmitool_path_entry.pack()

# 创建更新按钮
update_button = tk.Button(root, text="更新信息", command=update_info)
update_button.pack(pady=(10, 0))

update_ipmitool_button = tk.Button(root, text="更新IPMITOOL路径", command=update_ipmitool_path)
update_ipmitool_button.pack(pady=(10, 10))  # 额外的填充以区分按钮

# 运行主事件循环
root.mainloop()

while True:  # 创建一个无限循环
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
    # 注意：这里的命令和参数可能需要根据您的硬件和IPMI实现进行调整
    # '00 00' 可能是地址或特定于实现的参数，'f'{speed:02x}' 是速度值
    # 请确保这些值适合您的硬件
      cmd = ['raw', '0x2e', '0x30', '00', '00', f'{speed:02x}']
      subprocess.run([ipmitool_path, '-I', 'lanplus', '-H', ip, '-U', username, '-P', password] + cmd, check=True)


  def main():
      ip = '192.168.8.180'
      username = 'albert'
      password = 'admin'

      temp = get_cpu_temp(ip, username, password)
      if temp is not None:
          print(f"CPU Temperature: {temp}°C")

          if temp <= 39:
            set_fan_speed(ip, username, password, 20)
            print("success20")  # 假设 20 是某个代表 20% 的速度值
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


  time.sleep(100)
  # 调用 main 函数
  if __name__ == "__main__":
      main()


