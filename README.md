# HR-PRIME - Парсер вакансий с hh.ru

Сервис для сбора, анализа и экспорта данных о вакансиях с hh.ru. Собирает вакансии по регионам России, сохраняет в PostgreSQL и предоставляет API для работы с данными.

## 🚀 Возможности

- 🔍 Парсинг вакансий с hh.ru по регионам
- 💾 Сохранение в PostgreSQL с автоматическим созданием компаний
- 📊 Топ-20 компаний по количеству вакансий
- 📁 Экспорт в Excel
- 🐳 Docker-контейнеризация

## 🛠️ Технологии

- **Python 3.13**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL** - база данных
- **Pandas/OpenPyXL** - экспорт в Excel
- **Docker** - контейнеризация
- **Poetry** - управление зависимостями

## 📦 Установка

### Локальная установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd HR-PRIME-tz

# Установка зависимостей через Poetry
poetry install

# Создание .env файла
cp .env.example .env

# Запуск PostgreSQL через Docker
docker-compose up -d

# Запуск приложения
poetry run python main.py