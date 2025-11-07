# 🛍️ E-Commerce Product Management API

A robust **E-Commerce Product Management API** built with **Django REST Framework (DRF)**, designed to manage merchants, products, and product variants efficiently.  
This project demonstrates **clean architecture**, **scalable design patterns**, and **solid backend engineering practices**.

---

## 🚀 Overview

This API allows merchants to import products from external platforms (e.g., Shopify), manage their catalog, and perform bulk operations.  
It was designed focusing on:

- **Performance**: Efficient database operations using `select_related`, `prefetch_related`, and `bulk_create`.
- **Clarity**: Clean separation between services, serializers, and views.
- **Scalability**: Modular and easily extendable architecture.
- **Best Practices**: Following Django/DRF standards for code quality, error handling, and validation.

---

## 🏗️ Architecture Overview

- **Models** define the core business entities (Merchant, Product, Variant).
- **Serializers** handle data validation and transformation between Python objects and JSON.
- **Services** encapsulate business logic like importing products efficiently.
- **ViewSets** manage API endpoints, applying pagination, filtering, and error handling.

---

## 🧩 Tech Stack

- **Backend:** Django 5.1, Django REST Framework 3.15.2  
- **Database:** PostgreSQL (hosted on [Supabase](https://supabase.com))  
- **ORM:** Django ORM  
- **Docs:** drf-yasg (Swagger/OpenAPI auto-documentation)  
- **Config:** python-decouple for environment management  
- **CORS:** django-cors-headers for cross-origin resource sharing

---

**Main design principles:**
- Clear separation of concerns (Models, Serializers, Views, Services)
- Reusable and testable service layer
- RESTful and consistent endpoint design
- Readable, clean, and documented code following DRF best practices

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Framework** | Django 5.1 |
| **API Layer** | Django REST Framework (DRF) 3.15.2 |
| **Database** | PostgreSQL (Supabase) |
| **ORM** | Django ORM |
| **Documentation** | drf-yasg (Swagger/OpenAPI) |
| **Environment Management** | python-decouple |
| **CORS Handling** | django-cors-headers |

---

## 📦 Routes

| Method   | Endpoint              | Description                   |
| -------- | --------------------- | ----------------------------- |
| `POST`   | `/api/merchants/`      | Create a new merchant        |
| `POST`   | `/api/products/`      | Create a new product          |
| `GET`    | `/api/products/`      | List all products (paginated) |
| `GET`    | `/api/products/{id}/` | Retrieve a specific product   |
| `PUT`    | `/api/products/{id}/` | Update product details        |
| `DELETE` | `/api/products/{id}/` | Delete a product              |

## ⚙️ Setup & Run
🧾 Prerequisites

- Before running the project, make sure you have installed:

- Python 3.10+

- pip (Python package manager)

- virtualenv (recommended)

- PostgreSQL database (in this case, Supabase-hosted)

## 🧰 1️⃣ Clone the Repository
```
git clone https://github.com/ferreirawalter/django-api.git
cd django-api
```

## 🧩 2️⃣ Create and Activate Virtual Environment
### Create
```
python -m venv venv
```

### Activate (Windows)
```
venv\Scripts\activate
```

### Activate (Linux/Mac)
```
source venv/bin/activate
```

## 📦 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

## 🔑 4️⃣ Create .env File

In the root of your project, create a .env file and paste your Supabase credentials:
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=superpasswordtest123
DB_HOST=db.wiubhobxktnbtepbycqy.supabase.co
DB_PORT=5432
```

## 🛠️ 5️⃣ Apply Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

## 👤 6️⃣ Create Superuser (Optional, for Django Admin)
```
python manage.py createsuperuser
```

🚀 7️⃣ Run the Development Server
```
python manage.py runserver
```


The API will be available at:
👉 http://localhost:8000/api/