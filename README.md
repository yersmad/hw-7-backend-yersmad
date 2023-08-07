В этом задании мы перепишем наш маркетплейс цветов в API

Авторизация:

- `POST /signup` - обработчик для регистрации
- `POST /login` - обработчик входа по логину и паролю
- `GET /profile` - страница для показа информации о пользователе

Маршруты цветов:

- `GET /flowers` - для показа списка цветов
- `POST /flowers` - добавление цветов

Корзина:

- `POST /cart/items` - для добавления цветов в корзину (корзину хранить в куки)
- `GET /cart/items` - для получения списка цветов из корзины
- `POST /purchased` - обработчик который добавляет цветы из корзины в список купленных
- `GET /purchased` - для показа списка купленных цветов пользователя

---

## Задания

### 1. signup

- Реализовать обработчик регистрации `POST /signup`
    1. Сохранять пользователя в `UsersRepository`
    2. Возвращать `200 OK`
- Добавить возможность добавления фотографии пользователя при регистрации 💎

### 2. login

- Добавить `OAuth2PasswordBearer`
- Реализовать обработчик авторизации `POST /login`
    - Вернуть `{”access_token”: “<jwt>”, “type”: “bearer”}`
- Реализовать страницу показа информации о пользователе `GET /profile`
    1. Вернуть всю информацию о пользователе, кроме пароля

### 3. flowers

- Реализовать страницу `GET /flowers`
    - Вернуть список с цветами.
- Реализовать обработчик добавления цветов `POST /flowers`
    1. Сохранять цветок в FlowersRepository
    2. Возвращает id цветка

### 4. cart

- Реализовать `POST /cart/items`
    - Принимает параметр `flower_id: int = Form()`
    - Добавляет flower_id в куки
    - Возвращает `200 OK`
- Реализовать `GET /cart/items`
    - Возвращает список цветов находящихся в корзине
        - id
        - название цветов
        - стоимость
    - Отдельным полем показать общую сумму корзины
    

### 5. purchased 💎

- Реализовать `POST /purchased`
    - Добавляет все цветы из корзины в список купленных.
    - Каждый цветок закрепляется за пользователем в `PurchasesRepository`
    - `PurchasesRepository` хранит `Purchase(user_id, flower_id)`
    - Возвращает `200 ОК`
- Реализовать на `GET /purchased`
    - Вернуть список купленных цветов пользователя.
        - Название цветов
        - Стоимость цветов

## Замечания

- В репозиториях хранить классы, а не словари!
- Вы должны создать методы в репозиториях нужны для обработчиков