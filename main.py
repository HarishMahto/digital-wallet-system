from fastapi import FastAPI
from routes import users, wallet, transactions, products
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(wallet.router)
app.include_router(transactions.router)
app.include_router(products.router)