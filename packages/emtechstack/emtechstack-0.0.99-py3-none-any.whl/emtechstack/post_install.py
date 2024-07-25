import os
import subprocess
import sys
from pathlib import Path

def add_to_path():
    install_path = Path(sys.executable).parent
    current_path = os.environ['PATH']
    
    if str(install_path) not in current_path:
        # For Windows
        if os.name == 'nt':
            subprocess.call(f'setx PATH "{current_path};{install_path}"', shell=True)
            print("Added to PATH. Please restart your command prompt or terminal.")
        # For Unix-like systems
        else:
            print("Add the following to your ~/.bashrc or ~/.zshrc:")
            print(f'export PATH=$PATH:{install_path}')
            print("Then, source the file with 'source ~/.bashrc' or 'source ~/.zshrc'")



if __name__ == "__main__":
    add_to_path()