import os
import subprocess

# Hàm tự động khởi chạy Backend API Flask
def run_server_py():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(current_dir, 'Backend')
    server_script = 'server.py'
    os.chdir(backend_dir)
    subprocess.Popen(['python', server_script])
# Hàm tự động khởi chạy Frontend React JS
def run_npm_start():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(current_dir, 'Frontend')
    os.chdir(frontend_dir)
    # Sử dụng shell=True để thực thi lệnh npm start trong shell
    subprocess.Popen('npm start', shell=True)

if __name__ == '__main__':
    run_server_py()
    run_npm_start()
