# Каталог товаров на Django

Учебный проект: каталог с моделями `Category` и `Product`, база PostgreSQL, админка, фикстуры и команда для загрузки тестовых данных.

## Установка

```bash
poetry install
cp .env.sample .env        # затем впишите свои значения в .env
```

Создайте базу вручную (в psql):

```sql
CREATE DATABASE catalog_db;
```

## Запуск

```bash
python manage.py makemigrations catalog
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админка: http://127.0.0.1:8000/admin/

## Тестовые данные

Загрузить фикстуры вручную:

```bash
python manage.py loaddata category.json
python manage.py loaddata product.json
```

Или одной командой — она сначала удаляет все категории и продукты, затем загружает фикстуры:

```bash
python manage.py add_products
```

Выгрузить текущие данные в фикстуры (флаг `-Xutf8` нужен на Windows, чтобы кириллица сохранилась правильно):

```bash
python -Xutf8 manage.py dumpdata catalog.Category --indent 4 -o catalog/fixtures/category.json
python -Xutf8 manage.py dumpdata catalog.Product --indent 4 -o catalog/fixtures/product.json
```

## Структура

- `config/` — настройки проекта
- `catalog/models.py` — модели `Category` и `Product`
- `catalog/admin.py` — настройки админки
- `catalog/fixtures/` — фикстуры
- `catalog/management/commands/add_products.py` — кастомная команда
- `blog/` — приложение блога
- `screenshots/` — скриншоты работы в Django shell

## Блог

Приложение `blog`, адреса начинаются с `/blogs/`:

- `/blogs/` — список опубликованных статей
- `/blogs/create/` — новая статья
- `/blogs/<pk>/` — статья (при каждом открытии растёт счётчик просмотров)
- `/blogs/<pk>/update/` — редактирование, после сохранения открывается статья
- `/blogs/<pk>/delete/` — удаление

Все контроллеры `catalog` и `blog` написаны на классах (CBV).
