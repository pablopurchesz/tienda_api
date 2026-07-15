from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("", response_model=List[schemas.OrderOut])
def list_orders(email: Optional[str] = None, db: Session = Depends(get_db)):
    consulta = db.query(models.Order)
    if email is not None:
        consulta = consulta.filter(models.Order.customer_email == email)
    return consulta.all()

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    orden = db.query(models.Order).filter(models.Order.id == order_id).first()
    if orden is None:
        raise HTTPException(status_code=404, detail=f"Orden con id {order_id} no encontrada.")
    return orden

@router.post("", response_model=schemas.OrderOut, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    producto = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"No existe un producto con id {order.product_id}.")

    datos = order.model_dump()
    if datos["status"] is None:
        del datos["status"]
    else:
        datos["status"] = order.status.value

    nueva = models.Order(**datos)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(order_id: int, status_data: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    orden = db.query(models.Order).filter(models.Order.id == order_id).first()
    if orden is None:
        raise HTTPException(status_code=404, detail=f"Orden con id {order_id} no encontrada.")

    orden.status = status_data.status.value
    db.commit()
    db.refresh(orden)
    return orden

@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    orden = db.query(models.Order).filter(models.Order.id == order_id).first()
    if orden is None:
        raise HTTPException(status_code=404, detail=f"Orden con id {order_id} no encontrada.")

    db.delete(orden)
    db.commit()
