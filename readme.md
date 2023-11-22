# Программа для получения информации о погоде
- API, который на HTTP-запрос GET /weather?city=<city_name>, 
где <city_name> - это название города на русском языке, возвращает текущую температуру в этом городе 
в градусах Цельсия, атмосферное давление (мм рт.ст.) и скорость ветра (м/c). 
При первом запросе, сервис получает данные о погоде от yandex, 
при последующих запросах для этого города в течение получаса запросы на сервис yandex происходят
- Телеграм бот, который после нажатия кнопки "Узнать погоду" 
при получении названия города в ответ присылает прогноз погоды на сегодня
- Возможность просмотра в админке журнала запросов к API и сообщений к Телеграм боту
- Unit тесты

## Инструкция по запуску программы

Необходимо задать переменные окружения в файле `.env`. Пример можно найти в `.env.example`

### Локальный запуск

`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py runserver`

`python manage.py bot`

Протестировано на Ubuntu 22.04 с Python 3.10.10

### С помощью Docker

`docker compose up -d --build`

`docker compose run web python manage.py migrate`

`docker compose run web python manage.py createsuperuser`
