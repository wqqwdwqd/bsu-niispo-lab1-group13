# Управление многоконтейнерными системами

**БГУ · Факультет прикладной математики и информатики · НИиСПО**  
Лабораторная работа № 1. **Han Yu, группа 13**. Задания 1–4.

[Открыть отчёт](docs/report.md) · [32 контрольных вопроса с ответами](docs/control-questions.md) · [上传到 GitHub / Публикация](docs/submission.md)

| Задание | Что можно проверить | Файлы |
|---|---|---|
| 1 | Три версии Nginx и страница студента через bind mount | [index.html](task1/index.html) |
| 2 | Та же страница внутри опубликованного образа | [Dockerfile](task2/Dockerfile) · [Docker Hub](https://hub.docker.com/r/hy20010919/lab1-task2) |
| 3 | FastAPI, чтение и запись в PostgreSQL, семь вариантов образа | [Код и Dockerfile](task3/simple_python_app/) |
| 4 | Запуск Nginx, API и БД одной командой | [compose.yaml](task4/compose/compose.yaml) · [Конфигурация Nginx](task4/compose/nginx/app.conf) |

## Быстрая демонстрация задания 4

Требуются Docker Desktop в режиме Linux-контейнеров либо Docker Engine с современным модулем Compose и BuildKit. При первой сборке нужен доступ к реестру образов и индексу пакетов Python. Команды ниже рассчитаны на PowerShell. Начните в корне распакованного репозитория, рядом с этим README.

Если в Windows уже запущен Docker Desktop, а PowerShell не распознаёт команду `docker`, для пользовательской установки добавьте каталог команд в текущий сеанс:

```powershell
$dockerBin = Join-Path $env:LOCALAPPDATA 'Programs\DockerDesktop\resources\bin'
if (Test-Path "$dockerBin\docker.exe") { $env:Path = "$dockerBin;$env:Path" }
docker version
```

В корне проекта выполните:

```powershell
Set-Location task4/compose
if (!(Test-Path .env)) {
    "POSTGRES_PASSWORD=$([guid]::NewGuid().ToString('N'))" | Set-Content .env -Encoding ascii
}
docker compose config --quiet
docker compose up -d --build --wait
docker compose ps
```

Именованный том хранит БД между запусками. Сохраняйте созданный `.env` вместе с локальным стендом. Если порт 8085 занят, задайте `WEB_PORT=18085` отдельной строкой в `.env` и используйте выбранный порт в адресах ниже. В Linux вместо блока PowerShell для первого создания файла можно выполнить `test -f .env || echo "POSTGRES_PASSWORD=$(openssl rand -hex 24)" > .env` в каталоге `task4/compose`.

Откройте главную страницу: поле `postgres_version` берётся из SQL-запроса к БД. Через Swagger UI можно выполнить POST и сразу прочитать результат. [Главная](http://localhost:8085/) · [Swagger UI](http://localhost:8085/docs)

```powershell
curl.exe -fsS http://localhost:8085/
curl.exe -fsS http://localhost:8085/hello/Han
curl.exe -fsS -X POST http://localhost:8085/items/test
curl.exe -fsS http://localhost:8085/items
```

Каждый POST добавляет строку. Сопоставьте `id` из ответа POST с записью в списке GET. Если сервис ещё загружается, повторите запрос через несколько секунд. Вывод `docker compose logs --tail 50` поможет найти причину ошибки.

- `docker compose down` останавливает стенд и сохраняет том. После `docker compose up -d --wait` запись должна читаться снова.
- `docker compose down -v` завершает опыт **с удалением данных** текущего проекта. Проверьте `docker compose ps -a`, когда нужен показ очистки.

## Задания 1–3 по отдельности

Следующие блоки запускаются из корня репозитория на чистом стенде. Если вы только что выполняли задание 4 из этой инструкции, вернитесь командой `Set-Location ../..`. На компьютере с действующим стендом сначала выполните `docker ps -a`. Если контейнеры из таблицы уже работают, переходите к запросам проверки.

### 1. Nginx и каталог с HTML

```powershell
docker run -d --name mynginxlast -p 127.0.0.1:8080:80 nginx:latest
docker run -d --name mynginxalpine -p 127.0.0.1:8081:80 nginx:alpine
docker run -d --name mynginx1-28 -p 127.0.0.1:8082:80 nginx:1.28
$sitePath = (Resolve-Path task1).Path
docker run -d --name mynginxsite -p 127.0.0.1:8083:80 --mount "type=bind,source=$sitePath,target=/usr/share/nginx/html,readonly" nginx:alpine
docker ps -a
docker image ls nginx
curl.exe -fsS http://localhost:8080/
curl.exe -fsS http://localhost:8083/
```

Чтобы открыть оболочку в работающем Nginx, выполните `docker exec -it mynginxlast sh`. Внутри запустите `pwd` и `ls /usr/share/nginx/html`, затем `exit`. Для показа интерактивного запуска от начала до конца выполните следующий блок по одной строке. В интерактивном `sh` введите `pwd` и `exit`, затем выполните последние три команды в PowerShell.

```powershell
docker stop mynginxlast
docker rm mynginxlast
docker run --rm -it --name mynginxlast nginx:latest sh
docker run -d --name mynginxlast -p 127.0.0.1:8080:80 nginx:latest
docker stop mynginx1-28
docker start mynginx1-28
```

### 2. Страница в собственном образе

```powershell
docker build -f task2/Dockerfile -t lab1-task2:v1 task1
docker run -d --name mynginximage -p 127.0.0.1:8084:80 lab1-task2:v1
curl.exe -fsS http://localhost:8084/
```

Последний аргумент `task1` задаёт контекст, содержащий `index.html`. Для проверки публикации на другом компьютере выполните `docker pull hy20010919/lab1-task2:v1`. На стенде автора для публикации использовались `docker tag lab1-task2:v1 hy20010919/lab1-task2:v1` и `docker push hy20010919/lab1-task2:v1` после входа в Docker Hub.

### 3. Сборка семи образов

```powershell
Push-Location task3/simple_python_app
docker build -t simple_python_app:v1 -f Dockerfile .
docker build -t simple_python_app:v2 -f Dockerfile.v2 .
docker build -t simple_python_app:v3 -f Dockerfile.v3 .
docker build -t simple_python_app:v4 -f Dockerfile.v4 .
docker build -t simple_python_app:v5 -f Dockerfile.v5 .
docker build -t simple_python_app:v5-alpine -f Dockerfile.alpine .
docker build -t simple_python_app:v6 -f Dockerfile.v6 .
docker image ls simple_python_app
docker run --rm simple_python_app:v5 id
docker run --rm simple_python_app:v6 id
Pop-Location
```

### 3. Запуск API с БД без Compose

На новом стенде запустите PostgreSQL в пользовательской сети. Пароль создаётся один раз для пары контейнеров в текущем сеансе PowerShell. Клиенты обращаются к БД внутри сети по имени `postgres-db`.

```powershell
docker network create lab1-net
$labDbPassword = [guid]::NewGuid().ToString('N')
docker run -d --name postgres-db --network lab1-net -e "POSTGRES_PASSWORD=$labDbPassword" -e POSTGRES_DB=api -e POSTGRES_USER=apiuser postgres:16.2-alpine
docker exec postgres-db pg_isready -U apiuser -d api
```

Дождитесь ответа `accepting connections`, при необходимости повторите последнюю команду. Далее выполните в том же окне:

```powershell
docker run -d --name simple-python-api --network lab1-net -p 127.0.0.1:8001:8000 -e API_DB_HOST=postgres-db -e API_DB_USER=apiuser -e API_DB_NAME=api -e "API_DB_PASS=$labDbPassword" simple_python_app:v1
curl.exe -fsS http://localhost:8001/
curl.exe -fsS -X POST http://localhost:8001/items/test
curl.exe -fsS http://localhost:8001/items
```

Для повторной демонстрации уже созданных контейнеров достаточно `docker start postgres-db simple-python-api`. Дождитесь готовности БД перед запросом. В первичном опыте порт БД был опубликован на хосте как `5432:5432`. Для этих команд достаточно внутреннего порта. Для просмотра исходных результатов, включая размеры образов, откройте [отчёт](docs/report.md).
