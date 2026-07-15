# Tienda API

API REST para gestionar productos y órdenes de una tienda en línea, hecha con FastAPI, SQLAlchemy y PostgreSQL.

## Requisitos

- Python 3.11 o superior
- PostgreSQL corriendo en localhost (puerto 5432)

## Pasos para levantar el proyecto

### 1. Clonar el repositorio

```
git clone https://github.com/pablopurchesz/tienda_api.git
cd tienda_api
```

### 2. Crear y activar el entorno virtual

```
python -m venv venv
venv\Scripts\activate
```

(En Linux/Mac sería `source venv/bin/activate`)

### 3. Instalar las dependencias

```
pip install -r requirements.txt
```

### 4. Crear la base de datos

Entrar a PostgreSQL (por ejemplo con pgAdmin o con `psql -U postgres`) y crear la base:

```sql
CREATE DATABASE tienda_db;
```

Si tu usuario o contraseña de PostgreSQL son distintos, hay que cambiar la línea de conexión en `database.py`:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:TU_CONTRASEÑA@localhost:5432/tienda_db"
```

Las tablas (`products` y `orders`) se crean solas la primera vez que se levanta la API.

### 5. Levantar el servidor

```
uvicorn main:app --reload
```

La API queda corriendo en http://127.0.0.1:8000

## Documentación

Con el servidor corriendo, la documentación interactiva (Swagger) queda en:

http://127.0.0.1:8000/docs

## Endpoints

### Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /products | Lista todos los productos |
| GET | /products/{id} | Obtiene un producto por id |
| POST | /products | Crea un producto |
| PUT | /products/{id} | Actualiza un producto |
| DELETE | /products/{id} | Elimina un producto |

### Órdenes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /orders | Lista todas las órdenes |
| GET | /orders?email=... | Filtra órdenes por email del cliente |
| GET | /orders/{id} | Obtiene una orden por id |
| POST | /orders | Crea una orden |
| PUT | /orders/{id}/status | Actualiza el estado de una orden |
| DELETE | /orders/{id} | Elimina una orden |

Los estados válidos de una orden son: `pending`, `confirmed`, `shipped` y `cancelled`.

## Ejemplo rápido

Crear un producto:

```
curl -X POST http://127.0.0.1:8000/products -H "Content-Type: application/json" -d "{\"name\": \"Mouse Inalambrico\", \"description\": \"Mouse ergonomico\", \"price\": 15990, \"stock\": 50}"
```

Crear una orden:

```
curl -X POST http://127.0.0.1:8000/orders -H "Content-Type: application/json" -d "{\"customer_email\": \"cliente@example.com\", \"product_id\": 1, \"quantity\": 2}"
```
