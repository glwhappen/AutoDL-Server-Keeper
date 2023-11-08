import paramiko

import os
from dotenv import load_dotenv

load_dotenv()  # 这一行加载.env文件中的变量

ssh_password = os.getenv('SSH_PASSWORD')
def run_ssh(host, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=host, port=port, username=username, password=password)

        # 获取命令名称用于日志文件
        command_name = command.split('/')[-1]  # 假设命令路径最后一部分是文件名
        log_file_path = f'/root/log/{command_name}.log'

        # 修改命令来重定向输出到日志文件，并确保后台进程不会挂起SSH会话
        modified_command = f'nohup {command} > {log_file_path} 2>&1 & echo $!'
        stdin, stdout, stderr = client.exec_command(modified_command)

        # 读取PID输出
        pid = stdout.read().decode('utf-8').strip()
        if pid:
            print(f"FRP process started with PID: {pid}")
        else:
            error = stderr.read().decode('utf-8')
            print("Error:", error)

    finally:
        # 不等待命令完成，直接关闭客户端
        client.close()

if __name__ == '__main__':

    # 使用示例
    # 替换下面的参数为您的服务器的真实参数
    run_ssh(
        host='region-45.autodl.pro',
        port=35229,
        username='root',
        password=ssh_password,  # 替换为您的密码，并确保这个脚本在安全的环境中
        command='/root/frp_me/frpc -c /root/frp_me/frpc.ini'
    )
    run_ssh(
        host='region-45.autodl.pro',
        port=35229,
        username='root',
        password=ssh_password,  # 替换为您的密码，并确保这个脚本在安全的环境中
        command='/root/miniconda3/bin/python /root/autodl-fs/codegen/app.py'
    )