def create_state(path: str) -> str:
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
