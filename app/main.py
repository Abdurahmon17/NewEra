from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from database import engine, get_db
from models import Base, User, Product, Order, OrderDetail
from schemas import *
from auth import get_password_hash, verify_password, create_access_token, get_current_user

# Databasega migratsiya qilish
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="NewEra Cash & Carry",
    description="API for automating the NewEra Cash & Carry sales system",
    version="1.0.0",
)


# Auth bo'limi
@app.post("/auth/register", response_model=dict, tags=["Auth"])
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Foydalanuvchi allaqachon mavjud")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()

    return {"detail": "Foydalanuvchi ro'yxatdan o'tti"}


@app.post("/auth/login", response_model=dict, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Username yoki password xato!")
    token = create_access_token({"sub": user.username, "role": user.role.value})  # Convert role to string
    return {"access_token": token, "token_type": "bearer"}


# Products bo'limi
@app.get("/api/products", response_model=List[ProductResponseSchema], tags=["Products"])
async def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@app.post("/api/products", response_model=ProductResponseSchema, tags=["Products"])
async def create_product(product: ProductCreateSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Mijozlar uchun bu harakatga ruxsat berilmaydi.")
    
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/api/products/{product_id}", response_model=ProductResponseSchema, tags=["Products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Maxsulot topilmadi")
    return product


@app.put("/api/products/{product_id}", response_model=ProductCreateSchema, tags=["Products"])
async def update_product(product_id: int, product: ProductCreateSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Mijozlar uchun bu harakatga ruxsat berilmaydi.")
    
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Maxsulot topilmadi")

    for key, value in product.dict().items():
        setattr(existing_product, key, value)
    db.commit()
    db.refresh(existing_product)
    return existing_product


@app.delete("/api/products/{product_id}", response_model=dict, tags=["Products"])
async def delete_product(product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Mijozlar uchun bu harakatga ruxsat berilmaydi.")

    # Find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Maxsulot topilmadi")
    
    # Remove associated order details
    db.query(OrderDetail).filter(OrderDetail.product_id == product_id).delete()

    # Delete the product
    db.delete(product)
    db.commit()
    return {"message": "Mahsulot muvaffaqiyatli o'chirildi"}



# Orders bo'limi
@app.get("/api/orders", response_model=List[OrderResponseSchema], tags=["Orders"])
async def list_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    response = [
        OrderResponseSchema(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            items=[
                OrderDetailSchema(
                    product_id=detail.product_id,
                    quantity=detail.quantity
                )
                for detail in order.order_details
            ],
        )
        for order in orders
    ]
    return response


@app.post("/api/orders", response_model=OrderResponseSchema, tags=["Orders"])
async def create_order(order: OrderSchema, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.value not in ["admin", "customer"]:
        raise HTTPException(status_code=403, detail="Bu harakatga ruxsat berilmaydi.")
    
    new_order = Order(customer_id=current_user.id, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    order_items = []
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"{item.product_id} identifikatorli mahsulot topilmadi.")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"{product.name} mahsuloti uchun zaxira yetarli emas. Mavjud zaxira: {product.stock}"
            )

        product.stock -= item.quantity
        db.commit()
        
        order_detail = OrderDetail(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_detail)
        order_items.append(OrderDetailSchema(product_id=item.product_id, quantity=item.quantity))
    
    db.commit()

    return OrderResponseSchema(
        id=new_order.id,
        customer_id=new_order.customer_id,
        status=new_order.status,
        items=order_items
    )


@app.get("/api/orders/{order_id}", response_model=OrderSchema, tags=["Orders"])
async def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")

    if current_user.role.value not in ["admin", "customer"] and current_user.id != order.customer_id:
        raise HTTPException(status_code=403, detail="Bu harakatga ruxsat berilmaydi.")
    
    return OrderSchema(
        items=[OrderDetailSchema(product_id=detail.product_id, quantity=detail.quantity) for detail in order.order_details]
    )


@app.get("/api/customers/{customer_id}/orders", response_model=list[OrderResponseSchema], tags=["Orders"])
async def get_customer_orders(
    customer_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    if current_user.role.value != "admin" and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Mijozlar uchun bu harakatga ruxsat berilmaydi.")

    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .options(joinedload(Order.order_details))
        .all()
    )

    if not orders:
        raise HTTPException(status_code=404, detail="Bu foydalanuvchi uchun buyurtma topilmadi.")

    return [
        OrderResponseSchema(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            items=[
                OrderDetailSchema(
                    product_id=detail.product_id,
                    quantity=detail.quantity,
                )
                for detail in order.order_details
            ],
        )
        for order in orders
    ]


@app.get("/api/orders/{order_id}/status", response_model=dict, tags=["Orders"])
async def get_order_status(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")

    if current_user.role.value not in ["admin", "customer"] and current_user.id != order.customer_id:
        raise HTTPException(status_code=403, detail="Bu harakatga ruxsat berilmaydi.")
    
    return {"order_id": order.id, "status": order.status}


@app.put("/api/orders/{order_id}/status", response_model=dict, tags=["Orders"])
async def update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Buyurtma holatini faqat administratorlar yangilashi mumkin.")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Buyurtma topilmadi")

    valid_statuses = ["pending", "confirmed", "shipped", "completed", "canceled"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Yaroqsiz holat. Yaroqli holatlar: {', '.join(valid_statuses)}"
        )

    order.status = status
    db.commit()
    return {"message": f"Buyurtma holati “{status}” ga yangilandi"}