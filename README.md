# Enter: Управление алиасами и скриптами

Enter — это мощный инструмент для управления и выполнения алиасов и скриптов через командную строку. С его помощью вы можете автоматизировать рутинные задачи, упростить выполнение сложных команд и организовать свои скрипты в одном месте. Enter позволяет создавать, хранить и запускать команды с помощью простого и понятного YAML-конфигурационного файла.

## Установка

---

### Для Linux (Ubuntu)

- Установите Enter одной командой:
    ```bash
    bash <(curl -s https://raw.githubusercontent.com/morington/enter/dev/install.sh)
    ```

Этот скрипт:
- Установит все необходимые зависимости.
- Расположит исходный код в `~/.local/bin/enter`
- Создаст виртуальное окружение.
- Добавит команду `enter` в ваш `PATH`.
- Редактирование алиасов производится в файле `~/config_enter.yml`

### Для Windows

1. Убедитесь, что у вас установлен [Python 3.11](https://www.python.org/) или выше.
2. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
4. Активируйте виртуальное окружение::
    ```bash
    venv\Scripts\activate
    ```
5. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
6. Для удобного запуска создайте файл `enter.bat` внесите в него:
    ```bat
    @echo off
    set PYTHONPATH=C:\Users\<Ваше_имя>\.local\bin\enter
    C:\Users\<Ваше_имя>\.local\bin\enter\venv\Scripts\python.exe -m src.main.main %* 
    ```
7. Добавьте ваш файл `enter.bat` в переменные окружения

## Настройка конфигурации

---

Конфигурация Enter задаётся в YAML-файле (по умолчанию `~/config_enter.yml`). В этом файле вы можете определять скрипты и алиасы, которые будут доступны через команду `enter`.

Файл конфигурации указывается в `~/.local/bin/enter/config.ini`

### 1. **Скрипты**

---

Скрипты — это многострочные команды, которые можно вызывать внутри алиасов. Они полезны для выполнения повторяющихся задач.

#### Пример скрипта:

```yaml
scripts:
  gen_ssh_key: |
    if [ ! -f ~/.ssh/id_rsa ]; then
      echo "SSH key not found. Generating a new key..."
      ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N "" -q
      echo "SSH key successfully generated."
    else
      echo "SSH key already exists."
    fi
```

#### Как использовать скрипты:
- Скрипты вызываются внутри алиасов с помощью фигурных скобок: `{имя_скрипта}`.
- Скрипты могут содержать любые команды, которые поддерживаются вашей оболочкой (`bash`, `zsh` и т.д.).

### 2. **Алиасы**

---

Алиасы — это команды, которые могут принимать аргументы и использовать скрипты. Каждый алиас состоит из:
- Описания (`description`).
- Аргументов (`args` и `rargs`).
- Команд (`commands`).

#### Пример алиаса:

```yaml
aliases:
  hello:
    description: "Prints a greeting"
    args:
      name:
        description: "User's name"
        default: "Guest"
    rargs:
      place:
        description: "Place to greet the user"
    commands: |
      echo "Hello, {name}!"
      echo "Welcome to {place}!"
```

#### Как использовать алиасы:

- **Описание**: Показывается при вызове `enter --info <alias_name>`.
- **Аргументы**:
  - `args`: Опциональные аргументы (могут иметь значение по умолчанию).
  - `rargs`: Обязательные аргументы (без них команда не выполнится).
- **Команды**: Могут включать аргументы (пример: `{name}`) и скрипты (пример: `{gen_ssh_key}`).

#### Пример описания алиаса:

```bash
$ enter --info hello
Alias: hello
Description:
  Prints a greeting

[▼] Arguments:
  ▢ name [ Guest ] - User's name

[▼] Required Arguments:
  ▣ place* - Place to greet the user
```

### 3. **Аргументы**

---

Аргументы позволяют передавать данные в алиасы. Они могут быть:

- Опциональными (`args`): Имеют значение по умолчанию, которое используется, если аргумент не передан.
- Обязательными (`rargs`): Должны быть переданы, иначе команда завершится с ошибкой, но могут иметь значение по умолчанию, тогда ошибки не будет :)

#### Пример аргументов:

```yaml
args:
  name:
    description: "User's name"
    default: "Guest"  # Значение по умолчанию
rargs:
  place:
    description: "Place to greet the user"  # Обязательный аргумент
  user:
    description: "Test"
    default: 1  # Ошибки не будет, так как указан дефолтное значение
```

#### Как использовать аргументы:

Передавайте аргументы в формате ключ=значение:
```bash
enter hello name=John place=World
```

Если обязательный аргумент не передан, команда завершится с ошибкой:
```bash
$ enter hello name=John
🔴 Error: Missing required argument 'place'.
```

Если мы укажем лишний аргумент, он просто выдаст предупреждение, что аргумент не требуется
```bash
$ enter hello name=John place=Home a=aaa
2025-01-23 23:53:43 [EXECUTOR - warning] Argument is not required by the alias, but it was passed [execute.py:_merge_arguments:77] argument=a
Hello, John!
Welcome to Home!
```

При вызове аргумента `--debug` покажется полный трейс работы программы. **Для отладки.**
```bash
$ enter hello name=John place=Home --debug
2025-01-23 23:53:51 [MAIN - debug] Initializing                   [main.py:main:26]
2025-01-23 23:53:51 [YAML - debug] Alias configuration file found [yaml_repository.py:__init__:45] path=PosixPath('/home/user/config_enter.yml')
2025-01-23 23:53:51 [YAML - debug] Loaded scripts                 [yaml_repository.py:_parse_aliases:121] _count=1 scripts=['gen_ssh_key']
2025-01-23 23:53:51 [YAML - debug] Optional arguments received    [yaml_repository.py:_parse_aliases:133] _ALIAS=hello name="User's name"
2025-01-23 23:53:51 [YAML - debug] Required arguments received    [yaml_repository.py:_parse_aliases:134] _ALIAS=hello place='Place to greet the user'
2025-01-23 23:53:51 [YAML - debug] Optional arguments received    [yaml_repository.py:_parse_aliases:133] _ALIAS=generate_server_ssh_key
2025-01-23 23:53:51 [YAML - debug] Required arguments received    [yaml_repository.py:_parse_aliases:134] _ALIAS=generate_server_ssh_key
2025-01-23 23:53:51 [YAML - debug] Optional arguments received    [yaml_repository.py:_parse_aliases:133] _ALIAS=test
2025-01-23 23:53:51 [YAML - debug] Required arguments received    [yaml_repository.py:_parse_aliases:134] _ALIAS=test
2025-01-23 23:53:51 [YAML - debug] Loaded aliases                 [yaml_repository.py:_parse_aliases:146] _count=3 aliases=['hello', 'generate_server_ssh_key', 'test']
Hello, John!
Welcome to Home!
```

Дополнительно мы можем указать `-c` `--commands` для отображения построчного выполнения алиаса. **Для отладки.**
```bash
$ enter hello name=John place=Home -c
2025-01-24 00:25:43 [EXECUTOR - warning] Command execution display enabled [execute.py:execute:48]

> echo "Hello, John!"
Hello, John!

> echo "Welcome to Home!"
Welcome to Home!
```

### 4. **Команды**

---

Команды — это то, что выполняется при вызове алиаса. Они могут включать:

- **Текст**: Простые команды, такие как `echo`.
- **Аргументы**: Используйте `{имя_аргумента}` для подстановки значений.
- **Скрипты**: Используйте `{имя_скрипта}` для вызова скриптов.

#### Пример команд:

```bash
commands: |
  echo "Hello, {name}!"
  echo "Welcome to {place}!"
  {gen_ssh_key}  # Вызов скрипта
```

Используйте `|` для многострочных команд: Это позволяет писать длинные команды с переносами строк.


## Примеры использование

---

Примеры приведены с данным конфигурационным файлом алиасов:
```yaml
scripts:
  gen_ssh_key: |
    if [ ! -f ~/.ssh/id_rsa ]; then
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
    rargs:
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

### Список алиасов

```bash
$ enter --list
[▼] Available aliases:
  › hello: Prints a greeting
  › generate_server_ssh_key: Generate an SSH key
```

### Информация об алиасе

```bash
$ enter --info hello
Alias: hello
Description:
  Prints a greeting

[▼] Arguments:
  ▢ name [ Guest ] - User's name

[▼] Required Arguments:
  ▣ place* - Place to greet the user
```

### Выполнение алиаса

```bash
$ enter hello name=John place=World
🟢 Hello, John!
🟢 Welcome to World!
```

### Ошибка: Недостающий аргумент

```bash
$ enter hello name=John
🔴 Error: Missing required argument 'place'.
```

### Режим отладки

```bash
$ enter hello name=John place=World --debug
2025-01-23 23:53:51 [MAIN - debug] Initializing                   [main.py:main:26]
2025-01-23 23:53:51 [YAML - debug] Alias configuration file found [yaml_repository.py:__init__:45] path=PosixPath('/home/user/config_enter.yml')
2025-01-23 23:53:51 [YAML - debug] Loaded scripts                 [yaml_repository.py:_parse_aliases:121] _count=1 scripts=['gen_ssh_key']
2025-01-23 23:53:51 [YAML - debug] Optional arguments received    [yaml_repository.py:_parse_aliases:133] _ALIAS=hello name="User's name"
2025-01-23 23:53:51 [YAML - debug] Required arguments received    [yaml_repository.py:_parse_aliases:134] _ALIAS=hello place='Place to greet the user'
🟢 Hello, John!
🟢 Welcome to World!
```

## Благодарности

---

### Этот проект вдохновлён инструментом [Just](https://github.com/casey/just), созданным Casey. Спасибо за вдохновение и идеи!

## Автор

---

### Проект разработан и поддерживается [morington](https://github.com/morington).