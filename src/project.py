import configparser
import os, sys
import argparse
from .utils import ProjectTools


class ProjectCLI:

    VERSION = "project 1.0.0"
    CONFIG_INI = "project.ini"

    TOOLS = ProjectTools()

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

    def __config(self):
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
            requirements = self.config[_type]["requirements"].split("|")
            return requirements
        return None

    def __exists_args(self, parser):
        def poped_dict(d, k):
            d.pop(k)
            return d

        kwargs = dict(parser._get_kwargs())
        kwargs = (
            kwargs
            if kwargs["project_dir"] != "."
            else poped_dict(kwargs, "project_dir")
        )
        kwargs = (
            kwargs if kwargs["auto"] == True else poped_dict(kwargs, "auto")
        )
        kwargs = kwargs if kwargs["type"] else poped_dict(kwargs, "type")
        kwargs = (
            kwargs if kwargs["no_types"] else poped_dict(kwargs, "no_types")
        )
        kwargs = (
            kwargs
            if kwargs["projectname"]
            else poped_dict(kwargs, "projectname")
        )

        if kwargs:
            return True
        return False

    def __is_valid_type(self, _type):
        return any(ty for ty in self.config if ty == _type)

    def __print_types(self):
        valid_types = "\033[00m\n- \033[96m".join(
            [k for k in self.config if k != "DEFAULT"]
        )
        print(f"\n Pyproject Accept Types:\n- \033[96m{valid_types}")

    def __get_commands(self, _type):
        commands = self.config[_type]["command"].split("||")
        return commands

    def __init__(self):
        self.__config()
        if self.__load_project_ini(self.CONFIG_INI):
            self.__run()
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
            "-pd",
            "--project_dir",
            help='define em qual pasta será criada as dependencias, como o argumento final do "django-admin startproject (dir)", default="."',
            type=str,
            default=".",
        )
        self.parser.add_argument(
            "-at",
            "--no-types",
            help="Mostra todos os tipos de projetos aceitos",
            action="store_true",
            required=False,
        )

        parser_args = self.parser.parse_args()
        if parser_args and self.__exists_args(parser_args):
            _type = parser_args.type
            _auto = parser_args.auto
            _project_dir = parser_args.project_dir
            _no_types = parser_args.no_types
            _projectname = parser_args.projectname
            try:
                if _auto:
                    self.TOOLS.create_venv(_project_dir)
                    self.TOOLS.execute_command(self.__get_commands("default"))

                elif _no_types:
                    self.__print_types()
                    sys.exit(1)

                elif _type:
                    _type = _type.strip()
                    self.TOOLS.create_venv(_project_dir)
                    if self.__is_valid_type(_type):
                        pip = self.TOOLS.get_pipenv(_project_dir)
                        requirements = self.__get_requirements(_type)
                        self.TOOLS.install_requirements(pip, requirements)
                        if not _projectname:
                            _projectname = (os.getcwd().replace(
                                    os.path.dirname(os.getcwd()) + "\\", ""
                                ).lower().replace("-", "_")
                            )
                        _projectname = _projectname.strip()
                        commands = self.__get_commands(_type)
                        if _type in ("flask", "django"):
                            commands.append(f"{pip} freeze > requirements.txt")
                        if _type == "django":
                            pythonenv = self.TOOLS.get_pythonenv(_project_dir)
                            commands[1] = commands[1].format(projectname=_projectname, dir=_project_dir)
                            self.TOOLS.execute_command(commands, python=pythonenv)
                            sys.exit(1)
                        self.TOOLS.execute_command(commands)
                        sys.exit(1)
                    else:
                        raise ValueError(
                            f'Tipo de Projeto {_type} informado não é aceito, digite "pyproject --types" para mais informações!'
                        )
            except Exception as e:
                print("Argumento inválido: {}".format(e))
                sys.exit(1)
        else:
            self.parser.print_help()
            sys.exit(1)
