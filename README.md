# Тестовое задание для O-Комплекс
Тестовое задание - web приложение, оно же сайт, где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время

# Требования:
Сделать web приложение, оно же сайт, где пользователь вводит название города, и получает прогноз погоды в этом городе на ближайшее время.

 - Вывод данных (прогноза погоды) должен быть в удобно читаемом формате.

 - Веб фреймворк можно использовать любой.

 - api для погоды: https://open-meteo.com/ (можно использовать какое-нибудь другое, если вам удобнее)

# Технологии
* Сервис реализован на DjangoRestFramework
* Python версии 3.11
* База данных - PostgreSQL
- HTML/CSS - для создания пользовательского интерфейса
* ORM - DjangoORM
* Проект разворачивается с помощью docker compose
* Релизован pre-commit - при коммите код проверяется линтером и автоматически исправляются ошибки

## Установка и запуск:

# Предварительные условия

Предполагается, что пользователь установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине или на удаленном сервере, где проект будет запускаться в контейнерах. Проверить наличие можно выполнив команды:

```bash
docker --version && docker-compose --version
```
<h1></h1>

# Локальный запуск: Docker Compose

1. Клонируйте репозиторий с GitHub переменные окружения уже находятся в корневой папке проекта для удобства:

```bash
git clone git@github.com:LoG1s7/weather-forecast.git && \
cd weather-forecast&& \
```
2. Создайте файл ".env" в папке "weather-forecast". Пример наполнения в файле ".env.example"
```bash
cd weather-forecast && touch .env
```
3. Из корневой директории проекта выполните команду:
```bash
sudo docker compose -f infra/docker-compose.yml up -d --build
```
  Проект будет развернут в трех docker-контейнерах (db, web, nginx) по адресу http://localhost/api/.

4. Чтобы выполнить миграции выполните команду:
```bash
sudo docker compose -f infra/docker-compose.yaml exec web python manage.py migrate
```
5. Чтобы собрать статические файлы выполните команду:
```bash
sudo docker compose -f infra/docker-compose.yaml exec web python manage.py collectstatic --no-input
```
6. Чтобы создать суперюзера выполните команду и следуйте инструкции:
```bash
sudo docker compose -f infra/docker-compose.yaml exec web python manage.py createsuperuser
```
7. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
sudo docker compose -f infra/docker-compose.yml down
```
  Если также необходимо удалить том базы данных:
```bash
docker compose -f infra/docker-compose.yml down -v
```

#### URLS проекта и их описание
```bash
http://localhost/accounts/register - регистрация пользователя
http://localhost/accounts/login- аутентификация пользователя
http://localhost/accounts/logout- выход пользователя
http://localhost/weather/forecast - главная страница с прогнозом погоды
```
## Автор
[Aleksandr Kolesnikov](https://github.com/log1s7)
