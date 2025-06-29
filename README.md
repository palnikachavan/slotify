# 🗓️ Slot Booking App (Multi-Tenant SaaS Application)

An advanced **Slot Booking System** designed with multi-tenancy architecture to allow multiple companies or clinics to manage their own isolated bookings securely and independently.

### 🔍 Description

- Enables **companies or service providers** to register and manage their own slot booking systems.
- Each tenant gets a **dedicated PostgreSQL database**, ensuring **data isolation** and **scalability**.
- Fully API-driven backend for integration with frontend or mobile applications.

---

## 🛠️ Tech Stack Used

| Component         | Technology        |
|------------------|-------------------|
| Programming Language | Python 3.12+       |
| Framework        | Flask              |
| Database         | PostgreSQL         |
| ORM              | SQLAlchemy         |
| Authentication            | JWT, Werkzeug      |
| API Testing      | Postman            |
| Containerization (Optional) | Docker, Docker Compose |

---

## ✨ Features

- 🔐 **JWT Authentication** for tenant login & authorization
- 🏢 **Multi-Tenancy** using Database-per-Tenant approach
- 🛠️ **Service Management** (create, update, delete services)
- 📆 **Slot Management** (define available time slots)
- 👥 **User Slot Booking** for available services
- 🌐 **RESTful API** design
- 📁 Modular code structure for easy scalability

---

## 🚀 Installation

You can run the app in two ways:

---

### ✅ Option 1: Run with Docker

#### 📦 Step-by-Step

1. **Clone the Repository**

```bash
   git clone https://github.com/yourusername/slot-booking-app.git
   cd slot-booking-app
```


2. **Paste the following in your .env file and add required values**

```bash
   SECRET_KEY=
   JWT_EXPIRY_MINUTES=
   GLOBAL_ADMIN_EMAIL=
   GLOBAL_ADMIN_PASSWORD=

   # Do not change these
   ROLE_GLOBAL_ADMIN = global_admin
   ROLE_TENANT_ADMIN = tenant_admin
   ROLE_USER = user
```

3. **Run Docker Compose**


```bash
   docker-compose up --build
```

4. **App is running at**

```bash
   http://localhost:5000
```


5. **To stop containers**
```bash
   docker-compose down
```

### ✅ Option 2: Run without Docker

#### 📦 Step-by-Step

1. **Clone the Repository**

```bash
   git clone https://github.com/yourusername/slot-booking-app.git
   cd slot-booking-app
```

2. **Create Virtual Environment**

```bash
   python -m venv venv
   source venv/bin/activate
```

3. **Install Dependencies**

```bash
   pip install -r requirements.txt
```

4. **Paste the following in your .env file and add required values**
```bash
   SECRET_KEY=
   JWT_EXPIRY_MINUTES=
   GLOBAL_ADMIN_EMAIL=
   GLOBAL_ADMIN_PASSWORD=

   # Do not change these
   ROLE_GLOBAL_ADMIN = global_admin
   ROLE_TENANT_ADMIN = tenant_admin
   ROLE_USER = user
```

5. **Run the app**

```bash
   flask run
```