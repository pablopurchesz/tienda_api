from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    productos = db.query(models.Product).all()
    return productos

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Product).filter(models.Product.id == product_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto con id {product_id} no encontrado.")
    return producto

@router.post("", response_model=schemas.ProductOut, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    nuevo = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    producto = db.query(models.Product).filter(models.Product.id == product_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto con id {product_id} no encontrado.")

    producto.name = product_data.name
    producto.description = product_data.description
    producto.price = product_data.price
    producto.stock = product_data.stock

    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Product).filter(models.Product.id == product_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto con id {product_id} no encontrado.")

    db.delete(producto)
    db.commit()
