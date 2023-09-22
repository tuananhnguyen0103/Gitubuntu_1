import subprocess

script_path = 'run.py'  # Replace with the path to your Python script
result = subprocess.run(['python', script_path], check=True)
