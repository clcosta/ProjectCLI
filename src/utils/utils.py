import os
import shutil
import time
from typing import Optional


class ProjectTools:
    def create_venv(self, dir: str):
        def check_venv_alredy_exists():
            return os.path.exists(path)

        def check_pip_installed():
            return os.path.exists(
                os.path.abspath(os.path.join(path, "Scripts", "pip.exe"))
            )

        path = os.path.join(dir, "venv")
        if check_venv_alredy_exists():
            raise FileExistsError(
                "já existe um venv neste diretório {}".format(
                    os.path.abspath(dir)
                )
            )
        os.system("python -m venv {}".format(path))
        pip_installed = False
        count = 0
        while not pip_installed:
            if count == 30:  # 60s
                raise FileNotFoundError(
                    "Não foi possível encontrar o PIP, ocorreu um erro na instalação"
                )
            if check_pip_installed():
                pip_installed = True
            count += 1
            time.sleep(2)
        print(">> \033[92mvenv successfuly created!\033[00m")

    def execute_command(self, commands: list, python: Optional[str] = None, django: Optional[bool] = False):
        if python and django: commands[1] = commands[1].replace("django-admin", python + " -m django")
        
        for cmd in commands:
            os.system(cmd)
        print(">> \033[92mcommands successfuly executed!\033[00m")
        return
        
    def get_pythonenv(self, dir: str):
        return os.path.join(dir, "venv", "Scripts", "python.exe")

    def get_pipenv(self, dir: str):
        return os.path.join(dir, "venv", "Scripts", "pip.exe")

    def install_requirements(self, pip: str, requirements: list):
        if not requirements: return print(">> \033[92mrequirements not defined to this type!\033[00m")
        os.system(
            "{} install {}".format(pip, " ".join(requirements))
        )
        print(">> \033[92mrequirements successfuly created!\033[00m")
    
    def start_git(self, dir):
        if shutil.which('git.exe'):
            os.system("git init")
            print(">> \033[92mgit start in {}!\033[00m". format(os.path.relpath(dir)))
            return
        raise shutil.ExecError("git não foi encontra, verifique se ele foi adicionado ao PATH ou se está instalado corretamente")
