# Enter: Manage aliases and scripts

Enter is a powerful tool for managing and executing aliases and scripts via the command line. With it, you can automate routine tasks, simplify complex commands, and organize your scripts in one place. Enter allows you to create, store, and run commands using a simple, clean YAML configuration file.

## Installation

---

### For Linux (Ubuntu)

- Set Enter with one command:
    ```bash
    bash <(curl -s https://raw.githubusercontent.com/morington/enter/dev/install.sh)
    ```

This script:
- Installs all necessary dependencies.
- Will locate the source code in `~/.local/bin/enter`
- Creates a virtual environment.
- Adds the `enter` command to your `PATH`.
- Editing aliases is done in the file `~/config_enter.yml`

### For Windows

1. Make sure you have [Python 3.11](https://www.python.org/) or higher installed.
2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment::
    ```bash
    venv\Scripts\activate
    ```
5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. For convenient launch, create a file `enter.bat` and add to it:
    ```bat
    @echo off
    set PYTHONPATH=C:\Users\<Your_name>\.local\bin\enter
    C:\Users\<Your_name>\.local\bin\enter\venv\Scripts\python.exe -m src.main.main %* 
    ```
7. Add your `enter.bat` file to your environment variables

## Configuration settings

---

The Enter configuration is set in a YAML file (by default `~/config_enter.yml`). In this file you can define scripts and aliases that will be accessible through the `enter` command.

The configuration file is specified in `~/.local/bin/enter/config.ini`

### 1. **Scripts**

---

Scripts are multi-line commands that can be called inside aliases. They are useful for performing repetitive tasks.

#### Example script:
```yaml
scripts:
  gen_ssh_key: |
    if [! -f ~/.ssh/id_rsa ]; then
      echo "SSH key not found. Generating a new key..."
      ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -q
      echo "SSH key successfully generated."
    else
      echo "SSH key already exists."
    fi
```

#### How to use scripts:
- Scripts are called inside aliases using curly braces: `{script_name}`.
- Scripts can contain any commands that are supported by your shell (`bash`, `zsh`, etc.).

### 2. **Aliases**

---

Aliases are commands that can take arguments and use scripts. Each alias consists of:
- Descriptions (`description`).
- Arguments (`args` and `rargs`).
- `commands`.

#### Alias example:

```yaml
aliases:
  hello:
    description: "Prints a greeting"
    args:
      name:
        description: "User's name"
        default: "Guest"
    args:
      place:
        description: "Place to greet the user"
    commands: |
      echo "Hello, {name}!"
      echo "Welcome to {place}!"
```

#### How to use aliases:

- **Description**: Shown when calling `enter --info <alias_name>`.
- **Arguments**:
  - `args`: Optional arguments (may have a default value).
  - `rargs`: Required arguments (without them the command will not execute).
- **Commands**: Can include arguments (example: `{name}`) and scripts (example: `{gen_ssh_key}`).

#### An example of an alias description:

```bash
$ enter --info hello
Alias: hello
Description:
  Prints a greeting

[▼] Arguments:
  ▢ name [Guest] - User's name

[▼] Required Arguments:
  ▣ place* - Place to greet the user
```

### 3. **Arguments**

---

Arguments allow you to pass data to aliases. They may be:

- Optional (`args`): Have a default value that is used if no argument is passed.
- Required (`rargs`): Must be passed, otherwise the command will fail with an error, but can have a default value, then there will be no error :)

#### Example arguments:

```yaml
args:
  name:
    description: "User's name"
    default: "Guest" # Default value
args:
  place:
    description: "Place to greet the user" # Required argument
  user:
    description: "Test"
    default: 1 # There will be no error, since the default value is specified
```

#### How to use arguments:

Pass arguments in key=value format:
```bash
enter hello name=John place=World
```

If a required argument is not supplied, the command will fail with an error:
```bash
$ enter hello name=John
🔴 Error: Missing required argument 'place'.
```

If we specify an extra argument, it will simply issue a warning that the argument is not required
```bash
$ enter hello name=John place=Home a=aaa
2025-01-23 23:53:43 [EXECUTOR - warning] Argument is not required by the alias, but it was passed [execute.py:_merge_arguments:77] argument=a
Hello John!
Welcome to Home!
```

When calling the `--debug` argument, a complete trace of the program's operation will be displayed. **For debugging.**
```bash
$ enter hello name=John place=Home --debug
2025-01-23 23:53:51 [MAIN - debug] Initializing [main.py:main:26]
2025-01-23 23:53:51 [YAML - debug] Alias configuration file found [yaml_repository.py:__init__:45] path=PosixPath('/home/user/config_enter.yml')
2025-01-23 23:53:51 [YAML - debug] Loaded scripts [yaml_repository.py:_parse_aliases:121] _count=1 scripts=['gen_ssh_key']
2025-01-23 23:53:51 [YAML - debug] Optional arguments received [yaml_repository.py:_parse_aliases:133] _ALIAS=hello name="User's name"
2025-01-23 23:53:51 [YAML - debug] Required arguments received [yaml_repository.py:_parse_aliases:134] _ALIAS=hello place='Place to greet the user'
2025-01-23 23:53:51 [YAML - debug] Optional arguments received [yaml_repository.py:_parse_aliases:133] _ALIAS=generate_server_ssh_key
2025-01-23 23:53:51 [YAML - debug] Required arguments received [yaml_repository.py:_parse_aliases:134] _ALIAS=generate_server_ssh_key
2025-01-23 23:53:51 [YAML - debug] Optional arguments received [yaml_repository.py:_parse_aliases:133] _ALIAS=test
2025-01-23 23:53:51 [YAML - debug] Required arguments received [yaml_repository.py:_parse_aliases:134] _ALIAS=test
2025-01-23 23:53:51 [YAML - debug] Loaded aliases [yaml_repository.py:_parse_aliases:146] _count=3 aliases=['hello', 'generate_server_ssh_key', 'test']
Hello John!
Welcome to Home!
```

Additionally, we can specify `-c` `--commands` to display line-by-line execution of the alias. **For debugging.**
```bash
$ enter hello name=John place=Home -c
2025-01-24 00:25:43 [EXECUTOR - warning] Command execution display enabled [execute.py:execute:48]

> echo "Hello, John!"
Hello John!

> echo "Welcome to Home!"
Welcome to Home!
```

### 4. **Teams**

---

Commands are what is executed when an alias is called. These may include:

- **Text**: Simple commands such as `echo`.
- **Arguments**: Use `{argument_name}` to substitute values.
- **Scripts**: Use `{script_name}` to call scripts.

#### Example commands:

```bash
commands: |
  echo "Hello, {name}!"
  echo "Welcome to {place}!"
  {gen_ssh_key} # Call script
```

Use `|` for multiline commands: This allows you to write long commands with line breaks.


## Usage examples

---

Examples are given with this alias configuration file:
```yaml
scripts:
  gen_ssh_key: |
    if [! -f ~/.ssh/id_rsa ]; then
      echo "SSH key not found. Generating a new key..."
      ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -q
      echo "SSH key successfully generated."
    else
      echo "SSH key already exists."
    fi

aliases:
  hello:
    description: "Prints a greeting"
    args:
      name:
        description: "User's name"
        default: "Guest"
    args:
      place:
        description: "Place to greet the user"
    commands: |
      echo "Hello, {name}!"
      echo "Welcome to {place}!"

  generate_server_ssh_key:
    description: "Generate an SSH key"
    commands: |
      {gen_ssh_key}
```

### List of aliases

```bash
$ enter --list
[▼]Available aliases:
  › hello: Prints a greeting
  › generate_server_ssh_key: Generate an SSH key
```

### Alias information

```bash
$ enter --info hello
Alias: hello
Description:
  Prints a greeting

[▼] Arguments:
  ▢ name [Guest] - User's name

[▼] Required Arguments:
  ▣ place* - Place to greet the user
```

### Performing an alias

```bash
$ enter hello name=John place=World
🟢 Hello, John!
🟢Welcome to World!
```

### Error: Missing argument

```bash
$ enter hello name=John
🔴 Error: Missing required argument 'place'.
```

### Debug mode

```bash
$ enter hello name=John place=World --debug
2025-01-23 23:53:51 [MAIN - debug] Initializing [main.py:main:26]
2025-01-23 23:53:51 [YAML - debug] Alias configuration file found [yaml_repository.py:__init__:45] path=PosixPath('/home/user/config_enter.yml')
2025-01-23 23:53:51 [YAML - debug] Loaded scripts [yaml_repository.py:_parse_aliases:121] _count=1 scripts=['gen_ssh_key']
2025-01-23 23:53:51 [YAML - debug] Optional arguments received [yaml_repository.py:_parse_aliases:133] _ALIAS=hello name="User's name"
2025-01-23 23:53:51 [YAML - debug] Required arguments received [yaml_repository.py:_parse_aliases:134] _ALIAS=hello place='Place to greet the user'
🟢 Hello John!
🟢Welcome to World!
```

## Acknowledgments

---

#### This project is inspired by the tool [Just](https://github.com/casey/just) created by Casey. Thanks for the inspiration and ideas!

## Author

---

#### The project is developed and maintained by [morington](https://github.com/morington).