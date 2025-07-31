# Django CI/CD с GitHub Actions

В этом проекте настроен CI/CD с помощью **GitHub Actions** и **Docker**, который:

-  Автоматически запускает тесты при каждом `push`
-  Выполняет деплой на удалённый сервер, если тесты прошли успешно

---

## 🔁 Что происходит при push

1. Запускаются тесты
2.  Собирается Docker-образ и пушится в Docker Hub
3. Удалённый сервер подключается по SSH
4.  На сервере:
   - Образ загружается из Docker Hub
   - Прежний контейнер удаляется (если есть)
   - Запускается новый контейнер приложения


---

## 1. Настройка сервера (Ubuntu)
1. Откройте терминал и выполните команду для обновления списка пакетов:

sudo apt update

2. ООбновите пакеты до последней версии:

sudo apt update

3. Настройте файрфол:

sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

## Настройка GitHub Actions
Создайте файл .github/workflows/deploy.yml 

## Настройка паролей GitHub (Settings → Secrets → Actions)
SSH_KEY	приватный SSH-ключ
SSH_USER	SSH-пользователь (например ubuntu)
SERVER_IP	IP-адрес сервера
DOCKER_HUB_USERNAME	логин Docker Hub
DOCKER_HUB_PASSWORD	пароль Docker Hub
