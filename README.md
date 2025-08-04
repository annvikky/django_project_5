# Django CI/CD с GitHub Actions

В этом проекте настроен CI/CD с помощью **GitHub Actions** и **Docker**, который:

-  Автоматически запускает тесты при каждом `push`
-  Собирает и отправляет Docker-образ на Docker Hub
-  Деплоит на удалённый сервер, если тесты прошли успешно

---
## Развёрнутое приложение

Приложение доступно по адресу:  
**http://158.160.173.175/**  

---
## Что происходит при push

1. Запускается линтер `flake8`
2. Прогоняются Django-тесты (с базой PostgreSQL и Redis)
3. Собирается Docker-образ
4. Публикация образа на Docker Hub
5. По SSH подключение к серверу:
   - Скачивается новый образ
   - Старый контейнер удаляется
   - Запускается новый контейнер

---
## Локальный запуск проекта

1. **Клонировать репозиторий**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. Создать .env файл

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
LOCATION=redis://redis:6379/1

3. Запустить через Docker Compose

docker-compose up --build

4. Доступ к проекту

Приложение: http://localhost:8000

Админка: http://localhost:8000/admin/

# Настройка удалённого сервера (Ubuntu 20.04+)

## Обновление и установка Docker
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
### Настроить файрвол и SSH

sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

### Подготовить SSH-доступ
На своей машине:

ssh-keygen -t rsa -b 4096 -C "github-deploy"
cat ~/.ssh/id_rsa.pub  # и добавить на сервер в ~/.ssh/authorized_keys

# Настройка CI/CD
GitHub Actions
Файл workflow: .github/workflows/ci.yml

Основные этапы:
lint (flake8)
test (pytest / manage.py test)
build (docker image)
deploy (ssh + docker run) 

## Настройка паролей GitHub (Settings → Secrets → Actions)
SSH_KEY	приватный SSH-ключ
SSH_USER	SSH-пользователь (например ubuntu)
SERVER_IP	IP-адрес сервера
DOCKER_HUB_USERNAME	логин Docker Hub
DOCKER_HUB_PASSWORD	пароль Docker Hub
SECRET_KEY Django SECRET_KEY

# Полезные команды

## Логи контейнера
docker logs myapp
## Перезапуск контейнера
docker restart myapp
## Остановить и удалить контейнер
docker stop myapp && docker rm myapp
## Очистка dangling images
docker image prune -f
