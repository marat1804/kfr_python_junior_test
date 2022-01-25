# Тестовое задание Kefir


## Описание задачи
Разработать сервис для хранения данных о пользователях.

1. Аутентификация в сервисе происходит с помощью cookie.

2. Администраторы могут видеть все данные пользователей и изменять их.

3. Простые пользователи могут видеть лишь ограниченное число данных обо всех пользователях и редактировать часть своих данных.

[Спецификация API уже готова](https://github.com/marat1804/kfr_python_junior_test/blob/master/files/kfr_python_junior_test_openapi.json). Необходимо разработать сервис, который реализует этот API. 

## Реализация

- Использовались библиотеки Flask, Marshmallow и SQLAlchemy
- Для базы данных использовалась sqlite
- Создание существующего api в формате yaml с помощью apispec
- Swagger
- Unit - тестирование разработанного api с помощью pytest

## Добавленные или измененные конечные точки

- /users/{pk} изменен на /users/profile, для упрощения запросов со стороны front-end'а для текущего пользователя
- Добавлен /register для регистрации нового пользователя
- /refresh для обновления срока действия cookie для текущего пользователя
- /swagger-ui для доступа к Swagger'у
- /api для генерации api в формате yaml и получение его в формате json 

## Структура проекта

```
.
├── api             // файлы с api
├── app             // файлы приложения
│   ├── auth        // модуль с авторизацией и регистрацией
│   ├── common      // вспомогающие функции, модели для базы данных
│   ├── private     // модуль для администраторов
│   ├── swagger     // модуль для генерации api
│   └── users       // модель для пользователей
├── config          // конфигурация приложения
├── tests           // тесты
├── run.py          // точка входа в приложение
```


## Запуск проекта 

`python -m venv venv` - создание виртуального окружения  
`source venv/bin/activate` - активация виртуального окружения  
`pip install -r requirements.txt` - для установки всех необходимых зависимостей  
`python run.py` - для старта сервера  
`python -m pytest -v` - запуск тестов  
