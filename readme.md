# Советник

### Омниканальная платформа автоматизации приема и распределения обращений клиентов

## Структура проекта




## Алгоритм запуска

### С помощью докерg

```commandline
docker compose-up
```

### Локально на машине

1. Установка python 3.12

По ссылке скачайте [установщик](https://www.python.org/downloads/release/python-3120/) и следуюте инструкциям.

2. Установка зависимостей

```commandline
pip install -r requirements.txt
```

3. запуск кода

```commandline

```


Пример запроса:

```commandline
curl -X POST "https://billingweblab.ru.tuna.am/query" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Можете помочь с процессом банкротства",
           "service": "SIBINTEK_SYSTEM_PROMPT",
           "source": "vk",
           "chat_id": "123"
         }'
```