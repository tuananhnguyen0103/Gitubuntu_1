import platform
import subprocess

# Kiểm tra hệ điều hành đang chạy
current_os = platform.system()

if current_os == "Windows":
    # Mở một cửa sổ Command Prompt mới trên Windows
    subprocess.run(["start", "cmd"], shell=True)
elif current_os == "Linux":
    # Mở một cửa sổ Terminal mới trên Linux (bao gồm cả Ubuntu)
    subprocess.run(["gnome-terminal", "--"])  # Đối với GNOME Terminal
    # Hoặc subprocess.run(["xterm"]) nếu bạn sử dụng XTerm
elif current_os == "Darwin":
    # Mở một cửa sổ Terminal mới trên macOS
    subprocess.run(["open", "-n", "-a", "Terminal"])
else:
    print("Hệ điều hành không được hỗ trợ.")

