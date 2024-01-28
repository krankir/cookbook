# Cook Book
## Описание
Приложение поварской книги на Django

### Технологии
- Python
- Postgresql
- Django
- Docker

### Шаблон наполнения .env файла (создайте в корне проекта файл .env и заполните следующими данными)
- работаем с postgresql
```
DB_ENGINE=django.db.backends.postgresql 
```
- имя базы данных
```
DB_NAME=postgres
```
- пользователь базы данных
```
POSTGRES_USER=postgres
```
- пароль пользователя базы данных
```
POSTGRES_PASSWORD=postgres
```
- название контейнера
```
DB_HOST=db
```
- порт для работы с базой данных
```
DB_PORT=5432
```

### Запуск проекта в контейнерах Docker
- Перейдите в иеректорию с файлом docker-compose
```
docker-compose up -d --build 
```
- Создайте пользователя
```
docker-compose exec web python manage.py createsuperuser
```
- Заполнените базы данных тестовыми данными:
```
docker-compose exec web python manage.py loaddata ./fixtures/cookbook/product.json        
```
```
docker-compose exec web python manage.py loaddata ./fixtures/cookbook/recipe.json         
```
```
docker-compose exec web python manage.py loaddata ./fixtures/cookbook/productinrecipe.json
```

# Реализованные URL маршрутов:
- [admin^ка](http://127.0.0.1/admin) админка, где пользователь может управлять входящими в базу данных продуктами и рецептами. Для рецептов есть возможность редактировать входящие в их состав продукты и их вес в граммах.

### GET параметры вводить в строке url адресса после "?" разделяя несколько параметров знаком "&"
- [add_product_to_recipe](http://127.0.0.1/cookbook/add_product_to_recipe) с параметрами recipe_id, product_id, weight. Маршрут добавляет к указанному рецепту указанный продукт с указанным весом. Если в рецепте уже есть такой продукт, то функция должна поменять его вес в этом рецепте на указанный.
- [cook_recipe](http://127.0.0.1/cookbook/cook_recipe) c параметром recipe_id. Маршрут увеличивает на единицу количество приготовленных блюд для каждого продукта, входящего в указанный рецепт.
- [show_recipes_without_product](http://127.0.0.1/cookbook/show_recipes_without_product) с параметром product_id. Маршрут возвращает HTML страницу, на которой размещена таблица. В таблице отображены id и названия всех рецептов, в которых указанный продукт отсутствует, или присутствует в количестве меньше 10 грамм.

### Пояснения:
Проблема корректной работаты в случае одновременного доступа нескольких пользователей решена с помощью применения транзакций.

### Автор
Анатолий Редько

### License
MIT