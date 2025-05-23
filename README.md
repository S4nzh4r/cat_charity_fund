# **_QRKot_**
Приложение для Благотворительного фонда поддержки котиков QRKot.
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
Автор проекта обычный начинающий программист :/

Проект использует библиотеку FastAPI

Клонировать репозиторий и перейти в него в командной строке:

```
git clone твой ssh-ключ
```

```
cd cat_charity_fund/
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перед запуском проекта нужно проверить и применить миграций.
Миграций работают на библиотеке Alembic

```
# /alembic - Папка с миграциями
# /alembic/version - Все миграций проекта
# alembic.ini - Файл настроик Alembic, можно изменить его под свои нужды
# /alembic/env.py - Файл настроик для миграций

alembic --help # Команда для справки команд alembic
alembic revision --autogenerate -m "" # Автогенерация миграций с ключом -m для описания миграций
alembic upgrade head # Применить все не применённые миграций
alembic downgrade base # Откатить все миграций назад
```

Из корневой директорий проекта и запускаете проект через uvicorn:

```
# /cat_charity_fund

uvicorn app.main:app # Главное указать доступ к обьекту приложения
```

Для подробного ознакомления открывайте документацию на адресах:
```
/docs # Swagger
/redoc # Redoc

```