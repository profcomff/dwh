# Описание хранилища данных

## Наполнение
### Структура DDL

Папка struct предназначена для хранения DDL структуры хранилища.
Верхнеуровневые папки указывают тип таблицы:
- STG для данных, которые получаются из источника без
  дополнительной обработки;
- ODS для данных в процессе обработки, которые еще не могут быть
  использованы конечными пользователями, но которые могут
  понадобиться для разработки;
- DM для таблиц, предназначенных для конечных пользователей;
- APP для таблиц, которые нужны для работы приложений;

Структура внутри корневых папок:
- Название проекта
    - В UPPER_SNAKE_CASE;
    - Не транслит, а английский язык (проверяется ревьюером);
- Название таблицы
    - в UPPER_SNAKE_CASE;
    - Не транслит, а английский язык (проверяется ревьюером);
- Дата в формате YYYY-MM-DD
- Скрипты `up.sql` и `down.sql`
    - `up.sql` создает таблицу или обновляет предыдущую версию;
    - `down.sql` удаляет таблицу или возвращает к предыдущей версии;
    - (autogenerated) base.py содержит DDL таблицы после применения
      `up.sql` для проверок и экстренного восстановления базы.

Скрипт в папке `STG/TIMETABLE/TEST/2022-04-11` должен изменять таблицу
`STG_TIMETABLE.TEST` в базе данных.


## Локальное тестирование
Проверить правильность создания папок локально можно с помощью команды
```bash
python .github/utils/struct_test.py
```

## Описание CI/CD процесса
### Push
Операция push в репозиторий автоматически запускает проверку структуры файлов
и правильности скриптов `up.sql` и `down.sql`.

### Pull request Accepted
Операция pr в репозиторий производит проверку структуры файлов, правильности
скриптов `up.sql` и `down.sql` и сохранения получившегося после `up.sql`
состояния `base.sql`.
