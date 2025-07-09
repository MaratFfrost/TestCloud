# Cloud Storage Marketplace

Тестовое задание — агрегатор тарифных планов облачного хранения с возможностью оформления заказа.

## Описание

* **/plans** — получение агрегированных тарифов двух провайдеров (чтение из JSON-файлов)
* **/orders** — оформление заказа на тариф, отслеживание статуса (pending → complete)
* Модели — Pydantic
* Документация — Swagger/OpenAPI
* Тесты — pytest, httpx
* Хранение заказов — в памяти (in-memory)
* Эмуляция внешних провайдеров

---

## 📁 Структура проекта

```
app/
│
├── api/                # Роуты FastAPI
│   ├── orders.py
│   └── pricing_plans.py
│
├── models/             # Pydantic-модели
│   ├── order.py
│   └── pricing_plans.py
│
├── tasks/              # Background задачи
│   └── order.py
│
├── utils/              # Вспомогательные модули
│   └── storage.py
│
├── tests/              # Тесты (pytest)
│   ├── conftest.py
│   └── unit_tests/
│
├── main.py             # Точка входа FastAPI
│
├── Dockerfile          # Docker для продакшн
├── Dockerfile.dev      # Docker для разработки
├── requirements.txt    # Зависимости
├── docker-compose.yaml
├── docker-compose.redis.yml
└── pytest.ini
```

---

## 🚀 Быстрый старт через Docker

1. **Запусти Redis:**

   ```bash
   docker-compose -f docker-compose.redis.yml up -d
   ```

2. **Запусти приложение:**

   ```bash
   docker-compose up --build -d
   ```

3. **Сервис будет доступен по адресу:**

   * Приложение: [http://localhost:7788](http://localhost:7788)
   * Документация: [http://localhost:7788/docs](http://localhost:7788/docs)

---

## 📚 Эндпоинты

### Получить тарифные планы

```http
GET /plans?min_storage=50
```

**Параметры:**

* `min_storage` — минимальный объем (ГБ), по умолчанию 0

**Ответ:**
Список тарифов (агрегированные и отсортированные по полной стоимости).

---

### Оформить заказ

```http
POST /orders
```

**Пример запроса:**

```json
{
  "provider": "A",
  "storage_gb": 100
}
```

**Ответ:**

```json
{
  "order_id": "...",
  "status": "pending"
}
```

---

### Проверить статус заказа

```http
GET /orders/{order_id}
```

**Ответ:**

```json
{
  "order_id": "...",
  "status": "pending" | "complete"
}
```

---

## 🧪 Тестирование

```bash
pytest
```

---

## 💻 Локальный запуск (без Docker)

1. Установить зависимости:

   ```bash
   python -m venv venv
   source venv/bin/activate  # для Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Запустить Redis (например, через Docker):

   ```bash
   docker-compose -f docker-compose.redis.yml up -d
   ```

3. Измени в `main.py` строку подключения на:

   ```python
   redis_url = "redis://localhost:6379"
   ```

   *(или оставь REDIS\_HOST=localhost, если берёшь из переменных среды)*

4. Запусти приложение:

   ```bash
   uvicorn app.main:app --reload --port 7788
   ```

---

## 🔎 Примеры работы

**Получить тарифы**

```
GET http://localhost:7788/plans?min_storage=50
```

**Оформить заказ**

```
POST http://localhost:7788/orders
Body: { "provider": "A", "storage_gb": 100 }
```

**Проверить заказ**

```
GET http://localhost:7788/orders/{order_id}
```

---

