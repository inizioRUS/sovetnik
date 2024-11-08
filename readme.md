# Советник

### Омниканальная платформа автоматизации приема и распределения обращений клиентов

## Структура проекта

В папке llm находится реализация для подключения к кастомной нейронной сети или к OPENAI(Здесь нейронная сеть);

В папке milus находится реализация векторной базы данных, которая используется в реализации [RAG](https://habr.com/ru/articles/779526/)
мы используем предобученную модель/нейронную сеть для генерации векторов;

В папке pipelines находится сервисы для каждого клиента.


## Алгоритм запуска

### С помощью докерg

```commandline
docker compose-up
```

### Локально на машине

1. Установка python 3.12

По ссылке скачайте [установщик](https://www.python.org/downloads/release/python-3120/) и следуйюте инструкциям.

2. Установка зависимостей

```commandline
pip install -r requirements.txt
```

3. запуск кода

```commandline
unicorn main:app --host 0.0.0.0 --port 8007
```


Пример запроса:

```commandline
curl -X POST "https://billingweblab.ru.tuna.am/query" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Можете помочь с процессом банкротства",
           "service": "juridical",
           "source": "vk",
           "chat_id": "123"
         }'
```