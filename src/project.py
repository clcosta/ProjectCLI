import argparse
from ast import Tuple
import configparser
import os
import sys

from .utils import ProjectTools


class ProjectCLI:

    VERSION = "project 1.1.0"
    CONFIG_INI = "project.ini"

    tools = ProjectTools()

    def __load_project_ini(self, filename):
        full_path = os.path.abspath(os.path.join("./src", filename))
        path_file = (
            full_path
            if os.path.isfile(full_path)
            else os.path.abspath(
                os.path.join(os.path.dirname(sys.executable), filename)
            )
        )
        self.config = configparser.ConfigParser()
        if self.config.read(path_file):
            return True
        return False

    def __config_parser(self):
        self.parser = argparse.ArgumentParser(
            prog="pyproject",
            description="Cria um ambiente virtual e inicia um projeto Python!",
            epilog="Created By: Claudio Lima da Costa F.",
            usage="%(prog)s [options]",
        )

    def __run(self):
        self.parser.version = self.VERSION

    def __get_requirements(self, _type):
        if "requirements" in self.config[_type]:
            requirements = self.config[_type]["requirements"].split("||")
            return requirements
        return []

    def __exists_args(self, parser):
        return any(set(filter(lambda value: value if value != '.' else None ,[v for k, v in parser._get_kwargs()])))


    def __is_valid_type(self, _type):
        return any(ty for ty in self.config if ty == _type)

    def __print_types(self):
        valid_types = "\033[00m\n- \033[96m".join(
            [k for k in self.config if k != "DEFAULT"]
        )
        print(f"\n Pyproject Accept Types:\n- \033[96m{valid_types}")

    def __get_commands(self, _type):
        if "command" in self.config[_type]:
            commands = self.config[_type]["command"].split("||")
            return commands
        return []

    def __format_projectname(self, projectname):
        if not projectname:
            projectname = (os.getcwd().replace(os.path.dirname(os.getcwd()) + "\\", ""))
        return projectname.strip().lower().replace("-", "_")

    def __init__(self):
        self.__config_parser()
        if self.__load_project_ini(self.CONFIG_INI): self.__run()

        self.parser.add_argument(
            "-v", "--version", action="version", version=self.VERSION
        )
        self.parser.add_argument(
            "-a",
            "--auto",
            help="Cria o projeto default",
            action="store_true",
            required=False,
        )
        self.parser.add_argument(
            "-t",
            "--type",
            help='define o tipo de projeto e já instala as dependências (Opcional) - ex: "-t django"',
            type=str,
            required=False,
        )
        self.parser.add_argument(
            "-n",
            "--projectname",
            help="define o nome do projeto django que será criado",
            type=str,
            required=False,
        )
        self.parser.add_argument(
            "-d",
            "--projectdir",
            help='define em qual pasta será criada as dependencias, como o argumento final do "django-admin startproject (dir)", default="."',
            type=str,
            default=".",
        )
        self.parser.add_argument(
            "-at",
            "--all-types",
            help="Mostra todos os tipos de projetos aceitos",
            action="store_true",
            required=False,
        )
        self.parser.add_argument(
            "-wr",
            "--write-requirements",
            help="Faz o pip freeze nos requirements",
            action="store_true",
            required=False,
        )
        self.parser.add_argument(
            "-g",
            '--git',
            help="Iniciar um repositório git",
            action="store_true",
            required=False,
        )

        parser_args = self.parser.parse_args()
        if parser_args and self.__exists_args(parser_args):
            _type = parser_args.type
            _auto = parser_args.auto
            _projectdir = parser_args.projectdir
            _all_types = parser_args.all_types
            _projectname = parser_args.projectname
            _write_requirements = parser_args.write_requirements
            _git = parser_args.git
            try:
                if _git: self.tools.start_git(_projectdir)

                if _auto:
                    self.tools.create_venv(_projectdir)
                    self.tools.execute_command(self.__get_commands("default"))
                    sys.exit(0)

                elif _all_types:
                    self.__print_types()
                    sys.exit(0)

                elif _type:
                    _type = _type.strip()
                    if self.__is_valid_type(_type):
                        self.tools.create_venv(_projectdir)
                        pip = self.tools.get_pipenv(_projectdir)
                        requirements = self.__get_requirements(_type)
                        self.tools.install_requirements(pip, requirements)

                        _projectname = self.__format_projectname(_projectname)
                        
                        commands = self.__get_commands(_type)
                        if _write_requirements: commands.append(f"{pip} freeze > requirements.txt")
                        
                        match _type:
                            case "default":
                                self.tools.execute_command(commands)
                            case "django":
                                pythonenv = self.tools.get_pythonenv(_projectdir)
                                commands[1] = commands[1].format(projectname=_projectname, dir=_projectdir)
                                self.tools.execute_command(commands, python=pythonenv, django=True)
                            case _:
                                self.tools.execute_command(commands)
                        
                        sys.exit(0)
                    else:
                        raise ValueError(
                            f'Tipo de Projeto \"{_type}\" não é aceito, digite \033[0;33m"{self.parser.prog} --all-types"\033[00m para mais informações!'
                        )
            except Exception as e:
                print("Argumento inválido: {}".format(e))
                sys.exit(1)
        else:
            self.parser.print_help()
            sys.exit(0)