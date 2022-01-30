# Bem vindo ao **ProjectCLI**!
<p><img height="20" src="https://img.shields.io/badge/Version-v1.1.0-blue"/></p>

A criação de projetos python geralmente seguem um padrão. Como em todos meu projetos eu estava criando sempre os mesmos arquivos, pensei em automatizar o processo e facilitar minha vida. Uma CLI (Command Line Interface) tem o objetivo de conseguir ser acessada em qualquer pasta do seu computador direto pelo terminal, e com linhas de códigos pode executar funções e aplicativos.

## Redes Sociais
* [Instagram](https://www.instagram.com/claudiogfez/)
* [Linkedin](https://www.linkedin.com/in/clcostaf/)

# Pré requisitos
```
python 3.10.x
```
 **Está versão do python será utilizada na hora de gerar o .exe!**

## Instalação

1. É muito simples, você pode clonar este repositório.

```
git clone https://github.com/clcosta/ProjectCLI.git
```

## Como utilizar

### **O script neste momento já está funcionando!**
Pode-se executa-lo só digitando `python main.py` porém o objetivo é executar em qualquer pasta do computador. Sendo assim, é só criar um executável que será um arquivo adicionado ao PATH do computador e pode-se utilizar o script para ajudar a criar o executável, é só digitar o seguinte comando:

_Com este comando será criado um ambiente virtual no diretório atual, com a biblioteca **pyinstaller** já instalada_

```
python main.py --type installer
```

**OBS: A partir daqui esse código pode mudar para Sistemas Operacionais diferentes do _Windows_**

Agora é só ativar o ambiente virtual.

```
venv/scripts/activate
```

Com o Ambiente ativado, é só digitar o seguinte comando para transformar todo o código em um .exe

```powershell
pyinstaller --noconfirm --onefile --console --name "pyproject" --add-data "{SEU CAMINHO ATÉ O PROJETO}/ProjectCLI/src;src/"  "SEU CAMINHO ATÉ O ARQUIVO}/ProjectCLI/main.py"
```

Um diretorio com pasta dist será criada com seu executável, agora é só criar uma pasta no **Program Files** com o mesmo nome do .exe, geralmente o pogram files fica no **_'C:\Program Files\'_**. Com a pasta _pyproject_ criada só temos que adicionar o .exe e o arquivo de configuração **.ini** que está no **_.\src\project.ini_**. O Diretório ficará assim:

![diretorio](https://i.ibb.co/nLF64nT/image.png)

Agora é só adiciona-lo ao path do seu computador. Caso não saiba como fazer é só acessar este [link](https://stackoverflow.com/questions/4822400/register-an-exe-so-you-can-run-it-from-any-command-line-in-windows#answer-64233155)

**Agora a CLI já está funcionando como o esperado:**

![CLI](https://i.ibb.co/kqH7X0j/image.png)

### **Argumentos**

Qualquer um desses argumentos são listados com suas descrições no `--help`

| Argumento          | Exemplo                     |
| ------------------ | --------------------------- |
| help               | -h or --help                | 
| version            | -v or --version             |
| auto               | -a or --auto                | 
| type               | -t or --type                | 
| projectname        | -n or --projectname         | 
| projectdir         | -d or --projectdir          | 
| all-types          | -at or --all-types          | 
| write-requirements | -wr or --write-requirements | 
| git                | -g or --git                 | 

### **Exemplos de uso**

1. Cria um ambiente virtual sem nenhuma lib, um arquivo app.py e um requirements.txt (vazio)

```
pyproject -a
```

2. Cria um ambiente virtual com o django instalado, o arquivo do projeto django terá o nome "projeto_django", também cria os arquivos makefile (vazio) e requirements.txt (vazio), o diretorio do projeto será por default = '.'

```
pyproject -t django -n "projeto_django"
```

3. Cria um ambiente virtual com o flask instalado, será criado o arquivo requirements.txt com todas as dependências escritas nele. Um repositio git será iniciado nesta pasta

```
pyproject -t flask -g
```

### **Projetos Customizados**

Para criar projetos com suas dependencias e comandos customizados você pode adiciona-los ao arquivo **project.ini** que está localizado no **_.\src\project.ini_**. seguindo a seguinte logica:


_sempre separando os comandos e libs por pipes duplos "||"_
```ìni
[TIPO]
requirements=LIB1||lib2||LIB3
comand=echo comando pro terminal||touch comando.txt
```

**OBS: A CLI ainda não tem suporte para executar comandos utilziando o python do ambiente virtual em projetos de tipo customizados, atualmente está funcionalidade só está funcionando para projetos Django**

# Autor
| [<img src="https://avatars.githubusercontent.com/u/83929403?v=4" width=120><br><sub>@clcostaf</sub>](https://github.com/clcosta) |
| :---: |
