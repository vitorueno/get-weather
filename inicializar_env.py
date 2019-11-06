import os 
import platform


def criar_env():
    if platform.system() == "Windows":
        os.system('python -m venv env')
    elif platform.system() == "Linux":
        os.system('python3 -m venv env')

def ativar_env():
    if platform.system() == "Windows":
        os.system('call env/Scripts/activate')
            
    if platform.system() == "Linux":
        os.system('source env/Scripts/activate')

def baixar_requirements():
    if platform.system() == "Windows" or platform.system() == "Linux":
        os.system('python -m pip install -r requirements.txt')


if __name__ == "__main__":
    criar_env()
    ativar_env()