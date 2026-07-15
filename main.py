from fastapi import FastAPI

from database import engine, Base
import models
from routers import products, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tienda API")

app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def inicio():
    return {"message": "Tienda API funcionando. Visita /docs para la documentación interactiva."}
