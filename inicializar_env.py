import os 

def criar_env():
    os.system('python -m venv env')

def ativar_env():
    os.system('call env/Scripts/activate')
    
def baixar_requirements():
    os.system('python -m pip install -r requirements.txt')


if __name__ == "__main__":
    criar_env()
    ativar_env()
    baixar_requirements()