
# FastAPI Wallet System

A secure RESTful Digital Wallet backend built with **FastAPI**, supporting user registration, wallet funding, payments, currency conversion, product purchasing, and transaction history.

---

## Features

- User registration with **bcrypt password hashing**
- Basic Authentication for all secure endpoints
- Fund wallet, check balance, and pay other users
- Real-time **currency conversion** via [currencyapi.com](https://currencyapi.com)
- View full transaction history
- Product catalog with purchase workflow
- Postman collection & environment files provided

---

## Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLite** via SQLAlchemy
- **bcrypt** for password hashing
- **python-dotenv** for config
- **Uvicorn** as ASGI server

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/wallet_api.git
cd wallet_api
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup `.env` file

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///./wallet.db
CURRENCY_API_KEY=your_currencyapi_key_here
```

> You can get a free key from https://currencyapi.com

### 5. Run the server

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Testing

### Auth Note

All protected endpoints use **Basic Auth**:  
```http
Authorization: Basic base64(username:password)
```

In Postman, just use the `Authorization` tab > `Basic Auth`.

---

## API Endpoints

| Endpoint       | Method | Auth | Description                          |
|----------------|--------|------|--------------------------------------|
| `/register`    | POST   | ❌    | Create a new user                    |
| `/fund`        | POST   | ✅    | Add money to wallet                  |
| `/pay`         | POST   | ✅    | Pay another user                     |
| `/bal`         | GET    | ✅    | Check balance (optionally in USD)   |
| `/stmt`        | GET    | ✅    | Transaction history                  |
| `/product`     | POST   | ✅    | Add new product                      |
| `/product`     | GET    | ❌    | List all products                    |
| `/buy`         | POST   | ✅    | Buy a product using wallet balance   |

---

## Database

- Default: SQLite (file-based)

Run schema setup automatically on server start.

---

## Example Users

| Username | Password |
|----------|----------|
| `ashu`   | `hunter2` |
| `priya`  | `hunter2` |

---

Maintained by [Harish Mahto](https://github.com/HarishMahto)
