# Appvelox_RESTful_API_service

Для запуска проекта должно быть установлено следующее ПО:
- Django
- Django-CORS-headers
- Django REST Framework
- PostgreSQL
- Celery
- RabbitsMQ-server
- NodeJS
- npm
- Angular-http-server (устанавливается через npm для запуска клиентской части)
- Pillow

Для корректной работы REST-части проекта необходимо должным образом заранее настроить PostgreSQL, Celery и RabbitsMQ
и изменить настройки в файле settings.py соответствующим образом.

Описание тестов и используемых тестовых данных приведено в файлe проекта REST-части приложения API/tests/test.py. Тестовые данные необходимо изменять и наполнять
в соответстивии с записанными в файлы структурами формата JSON, расположенных в проекте REST-части приложения в директории API/tests/tests_data.

В тестироввании используется основная база данных REST-части приложения. Поэтому тесты необходимо запускать с помощью команды: python3 manage.py test --keepdb 

Клиентская часть проекта запускается через установленный локальный сервер angular-http-server в корне папки frontend c помощью команды "angular-http-server" на порту по умолчанию 8080. После запуска клиентская часть приложения будет доступна по адресу http://127.0.0.1:8080.

REST-часть проекта запускается типичным образом как и все Django-проекты. REST-часть проекта работает на порту 8000 и доступна по адресу http://127.0.0.1:8000.

URL-адреса для использования реализованного API:
- http://127.0.0.1:8000/api/v1/resizeImage - POST-запрос на обработку изображения
- http://127.0.0.1:8000/api/v1/statusImage/id - GET-запрос на получение текущего статуса выполнения задачи на обработку изображения. Где id - идентификатор задачи в формате UUID4
- http://127.0.0.1:8000/api/v1/download/id - GET-запрос на скачивание изображения с сервера приложения. Где id - идентификатор изображения в формате UUID4 (совпадает с идентификатором назначенной задачи)
