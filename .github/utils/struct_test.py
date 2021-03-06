import argparse
from os import walk
from typing import Dict, Set
from datetime import datetime


def parse_args():
    """Получить параметры командной строки."""
    parser = argparse.ArgumentParser(description="CI/CD в БД")
    parser.add_argument("--dsn", help="Строка подключения к БД")
    parser.add_argument(
        "--test-all",
        "-t",
        action="store_true",
        default=False,
        help="Протестировать, но не сохранять итоговые состояния",
    )
    parser.add_argument(
        "--state-all",
        "-s",
        action="store_true",
        default=False,
        help="Протестировать, и сохранить состояния",
    )
    parser.add_argument(
      "--produce-all",
      "-p",
      action="store_true",
      default=False,
      help="Запустить все новые up.sql"
    )
    return parser.parse_args()


def test_folder_structure(path='struct') -> bool:
    """Проверяем правильность папок в репозитории.

    Папка struct содержит скрипты для обновления базы дынных.
    Должна иметь следующую структуру:
        - Название среды:
            - STG для данных, которые получаются из источника без
              дополнительной обработки;
            - ODS для данных в процессе обработки, которые еще не могут быть
              использованы конечными пользователями, но которые могут
              понадобиться для разработки;
            - DM для таблиц, предназначенных для конечных пользователей;
            - APP для таблиц, которые нужны для работы приложений;
        - Название проекта
            - В UPPER_SNAKE_CASE;
            - Не транслит, а английский язык (проверяется ревьюером);
            - В папке должен находиться файл `schema.py` с SQL создания схемы;
        - Название таблицы
            - в UPPER_SNAKE_CASE;
            - Не транслит, а английский язык (проверяется ревьюером);
        - Дата в формате YYYY-MM-DD
        - Скрипты up.sql и down.sql
            - up.sql создает таблицу или обновляет предыдущую версию;
            - down.sql удаляет таблицу или возвращает к предыдущей версии;
            - (autogenerated) base.py содержит DDL таблицы после применения
              up.sql для проверок и экстренного восстановления базы.
    """
    tables: Dict[str, Set[str]] = {}
    warnings = list()
    errors = list()
    for subdir, dirs, files in walk(path):
        subdir = subdir.replace(path, '').strip('/')
        if subdir != subdir.upper():
            errors.append(f'Schema and table names should be uppercase {subdir}')
        subdir = subdir.split('/')

        # Проверка папок схем
        if len(subdir) == 2:
            tables[f'{subdir[0]}_{subdir[1]}'] = set()
            files = [f.lower() for f in files]
            if 'readme.md' not in files:
                warnings.append(f'No README.md in schema directory {"/".join(subdir)}')
            if 'schema.sql' not in files:
                errors.append(f'No schema.sql in schema directory {"/".join(subdir)}')

        # Проверка папок таблицы
        elif len(subdir) == 3:
            tables[f'{subdir[0]}_{subdir[1]}'].add(subdir[2])
            for dir in dirs:
                try:
                    datetime.fromisoformat(dir)
                except ValueError:
                    errors.append(f'Name not in timestamp format {"/".join([*subdir, dir])}')

        # Проверка папок версий
        elif len(subdir) == 4:
            if 'up.sql' not in files:
                errors.append(f'No up.sql in {"/".join(subdir)}')
            if 'down.sql' not in files:
                errors.append(f'No down.sql in {"/".join(subdir)}')

    for err in errors:
        print('[ERROR] ', err)
    for warn in warnings:
        print('[WARN] ', warn)

    return not bool(errors)


def test_nochanges(_) -> bool:
    """Проверка, что старые скрипты не изменялись.

    Дифф между корнем данной ветки и головой по up.sql/down.sql/state.sql.
    Чтобы не произошло такого, что на проде таблица с одним кодом, а
    в репозитории с другим.
    """


def test_noconflicts(_) -> bool:
    """Проверка, что не появилось обновленных версий тех же таблиц.

    Дифф между мастером и головой.
    Чтобы не произошло такого, что два человека отредактировали одну и ту
    же таблицу и они теперь конфликтуют.
    """


def create_state(_) -> str:
    """Получить DDL таблицы.

    В PostgreSQL есть команда, которая позволяет получить код таблицы по ее
    названию. Она используется, например, в DBeaver, чтобы показывать DDL
    таблиц. Возвращает текстовое представление таблице в виде:

    ```sql
    -- Drop table

    -- DROP TABLE dyakovri.stg_data;

    CREATE TABLE dyakovri.stg_data (
        id int4 NOT NULL,
        some_value varchar(512) NULL,
        CONSTRAINT stg_data_pkey PRIMARY KEY (id)
    );
    ```

    inputs
    ------
    path: str
        Путь к таблице

    outputs
    -------
        DDL таблицы
    """


def test_upgrade(_) -> bool:
    """Запуск скрипта увеличения версии в тестовом окружении.

    - Если таблица существует в тестовом окружении, ее надо удалить и создать
      заново из предпоследней версии `state.sql`. Если версия всего одна,
      пропустить шаг;
    - Запустить скрипт `up.sql` последней версии;
    - Выполнить `create_state` и записать в файл `base.py`.
    """


def test_downgrade(_) -> bool:
    """Запуск скрипта уменьшения версии в тестовом окружении.

    - Если таблица существует в тестовом окружении, ее надо удалить и создать
      заново из последней версии `state.sql`;
    - Запустить скрипт `down.sql` последней версии;
    - Выполнить `create_state` и сверить результат с предпоследней
      версией `base.py`.
    """


if __name__ == "__main__":
    args = parse_args()
    assert test_folder_structure(), "Folder structure incorrect"
    # assert test_nochanges(...), "Old scripts can't be changed"
    # assert test_noconflicts(...), "Old scripts can't be changed"
    # assert test_upgrade(...), "Upgrade script is incorrect"
    # assert test_downgrade(...), "Downgrade script is incorrect or wrong state"
    print("Test complete!")
