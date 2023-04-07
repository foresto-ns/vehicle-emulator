# vehicle-emulator

## Запуск сервиса

```
cd vehicle-emulator/
docker-compose up -d
```

## Использование сервиса
Использовать сервис можно как с использованием API методов,
так и через web-интерфейс по адресу http://localhost:8000/  
Также есть и админка для управления данными моделей http://localhost:8000/admin/login

Смотреть присылаемые статусы от ТС можно в логах:
- файл `receiver/log/DEBUG.log` 
- через команду `docker logs whoosh-receiver`

## API методы
Описание методов доступно по http://localhost:8000/api/swagger
