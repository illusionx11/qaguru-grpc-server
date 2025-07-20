# 📸 PhotoCatalog gRPC Server

Сервер для управления каталогом фотографий, реализованный на Python с использованием gRPC.

## 🚀 Возможности

- **Добавление фотографий** - загрузка новых фотографий с описанием
- **Получение фотографий** - поиск по уникальному ID
- **Случайные фотографии** - получение случайного набора фотографий
- **Пакетная загрузка** - стриминговый метод для загрузки множества фотографий

## 🏗️ Архитектура

```
qaguru-grpc-server/
├── app/
│   ├── main.py                 # Точка входа сервера
│   └── service/
│       └── photocatalog/
│           ├── service.py      # gRPC сервис
│           ├── protocol.py     # Интерфейс репозитория
│           └── mock_repository.py # In-memory репозиторий
├── internal/
│   └── pb/                    # Сгенерированные protobuf файлы
├── protos/
│   └── photocatalog.proto     # Определение gRPC сервиса
└── requirements.txt           # Зависимости Python
```

## 📋 Требования

- Python 3.8+
- pip
- virtualenv (рекомендуется)

## 🔧 Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd qaguru-grpc-server
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Сгенерируйте protobuf файлы:**
   ```bash
   python -m grpc_tools.protoc \
     -I./protos \
     --python_out=./internal/pb \
     --pyi_out=./internal/pb \
     --grpc_python_out=internal/pb \
     ./protos/photocatalog.proto
   ```

## 🚀 Запуск

Запустите сервер:
```bash
python app/main.py
```

Сервер будет доступен на `localhost:50051`

## 📡 API Методы

### 1. Photo - Получение фотографии по ID
```protobuf
rpc Photo(IdRequest) returns (PhotoResponse)
```

**Запрос:**
```json
{
  "id": "uuid-фотографии"
}
```

**Ответ:**
```json
{
  "id": "uuid-фотографии",
  "description": "Описание фотографии",
  "timestamp": "2024-01-01T12:00:00Z",
  "content": "base64-данные-фотографии"
}
```

### 2. AddPhoto - Добавление одной фотографии
```protobuf
rpc AddPhoto(PhotoRequest) returns (PhotoResponse)
```

**Запрос:**
```json
{
  "description": "Описание фотографии",
  "content": "base64-данные-фотографии"
}
```

### 3. RandomPhotos - Получение случайных фотографий
```protobuf
rpc RandomPhotos(CountRequest) returns (stream PhotoResponse)
```

**Запрос:**
```json
{
  "count": 5
}
```

### 4. UploadPhotos - Пакетная загрузка фотографий ⭐
```protobuf
rpc UploadPhotos(stream PhotoUploadRequest) returns (UploadResponse)
```

**Запрос (стрим):**
```json
[
  {
    "description": "Фото 1",
    "content": "base64-данные-1"
  },
  {
    "description": "Фото 2", 
    "content": "base64-данные-2"
  }
]
```

**Ответ:**
```json
{
  "success": true,
  "message": "Количество загруженных фотографий: 2",
  "uploaded_count": 2
}
```

## 🧪 Тестирование

### С помощью Postman

1. **Настройте gRPC запрос в Postman:**
   - URL: `localhost:50051`
   - Service: `PhotoCatalogService`
   - Method: `UploadPhotos`

2. **Пример данных для UploadPhotos:**
   ```json
   [
     {
       "description": "Красивый закат",
       "content": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
     },
     {
       "description": "Горный пейзаж", 
       "content": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
     }
   ]
   ```

### С помощью Python клиента

Создайте файл `test_client.py`:

```python
import grpc
import internal.pb.photocatalog_pb2 as pb2
import internal.pb.photocatalog_pb2_grpc as pb2_grpc

def test_upload():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.PhotoCatalogServiceStub(channel)
        
        def photo_stream():
            photos = [
                {"description": "Тест 1", "content": "data:image/jpeg;base64,..."},
                {"description": "Тест 2", "content": "data:image/jpeg;base64,..."}
            ]
            for photo in photos:
                yield pb2.PhotoUploadRequest(**photo)
        
        response = stub.UploadPhotos(photo_stream())
        print(f"Результат: {response.message}")

if __name__ == "__main__":
    test_upload()
```

## 📦 Зависимости

- `grpcio-tools==1.73.1` - Генерация protobuf/gRPC кода
- `pydantic==2.11.7` - Валидация данных
- `grpcio-reflection==1.73.1` - Reflection API

## 🔄 Разработка

### Добавление новых методов

1. **Обновите proto файл** (`protos/photocatalog.proto`)
2. **Сгенерируйте protobuf файлы:**
   ```bash
   python -m grpc_tools.protoc -I./protos --python_out=./internal/pb --pyi_out=./internal/pb --grpc_python_out=internal/pb ./protos/photocatalog.proto
   ```
3. **Реализуйте метод в сервисе** (`app/service/photocatalog/service.py`)

### Структура проекта

- **`app/main.py`** - Точка входа, запуск gRPC сервера
- **`app/service/photocatalog/service.py`** - Реализация gRPC методов
- **`app/service/photocatalog/protocol.py`** - Интерфейсы (Protocol)
- **`app/service/photocatalog/mock_repository.py`** - In-memory хранилище
- **`internal/pb/`** - Автогенерированные protobuf файлы
- **`protos/photocatalog.proto`** - Определение gRPC API

## 🐛 Устранение неполадок

### Ошибка импорта модуля `internal`
```bash
ModuleNotFoundError: No module named 'internal'
```
**Решение:** Убедитесь, что запускаете сервер из корневой директории проекта.

### Ошибка gRPC методов
```bash
'_Context' object has no attribute 'set_node'
```
**Решение:** Используйте `context.abort()` вместо `context.set_node()`.

## 📄 Лицензия

Проект распространяется под лицензией, указанной в файле `LICENSE`.

---

**🎯 Готово к использованию!** Сервер поддерживает все основные операции с фотографиями, включая новый стриминговый метод для пакетной загрузки.