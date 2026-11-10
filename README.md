# Gym Management API

A Django REST API for running a gym. It stores trainers, members, membership plans, memberships, and payments. Users register and sign in with JSON Web Tokens (JWT). Every other endpoint requires an authenticated user.

## Stack

- Python 3.12
- Django 6.1.3
- Django REST Framework 3.18.3
- djangorestframework-simplejwt 5.5.1
- SQLite

## What it covers

- Public user registration and JWT access and refresh tokens
- Full create, read, update, and delete for trainers, members, plans, memberships, and payments
- Django admin for the same models

## Layout

```
gym_management/
├── config/          # settings, root URLs, WSGI and ASGI
├── gym/             # models, serializers, viewsets, and API routes
├── manage.py
└── db.sqlite3       # local SQLite database
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install "Django==6.1.3" "djangorestframework==3.18.3" "djangorestframework-simplejwt==5.5.1"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is at `http://127.0.0.1:8000/`. The browsable API is available in the browser when you are signed in. Django admin is at `http://127.0.0.1:8000/admin/`.

`DEBUG` is on and the database is SQLite. These settings are for local development.

## Authentication

Registration and the token routes are public. Everything else uses the default permission `IsAuthenticated`. Send either a JWT bearer token or HTTP Basic credentials.

Register a user:

```http
POST /api/register/
Content-Type: application/json

{
  "username": "alex",
  "email": "alex@example.com",
  "password": "strongpass1"
}
```

`password` is write-only and must be at least 8 characters. Django's password validators also apply.

Get tokens:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "alex",
  "password": "strongpass1"
}
```

The response includes `access` and `refresh`. Send the access token on later requests:

```http
Authorization: Bearer <access>
```

Refresh an access token:

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh>"
}
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST | `/api/register/` | Create a user. Public. |
| POST | `/api/token/` | Obtain access and refresh tokens. Public. |
| POST | `/api/token/refresh/` | Refresh an access token. Public. |
| GET, POST | `/api/trainers/` | List or create trainers |
| GET, PUT, PATCH, DELETE | `/api/trainers/{id}/` | Read, update, or delete a trainer |
| GET, POST | `/api/members/` | List or create members |
| GET, PUT, PATCH, DELETE | `/api/members/{id}/` | Read, update, or delete a member |
| GET, POST | `/api/plans/` | List or create membership plans |
| GET, PUT, PATCH, DELETE | `/api/plans/{id}/` | Read, update, or delete a plan |
| GET, POST | `/api/memberships/` | List or create memberships |
| GET, PUT, PATCH, DELETE | `/api/memberships/{id}/` | Read, update, or delete a membership |
| GET, POST | `/api/payments/` | List or create payments |
| GET, PUT, PATCH, DELETE | `/api/payments/{id}/` | Read, update, or delete a payment |

## Models

**Trainer.** `full_name`, unique `email`, `phone`, `specialization`, `experience` (years), `is_active` (default `true`), and `created_at`.

**Member.** One-to-one `user`, optional `trainer`, `phone`, `age`, `joined_date`, and `is_active` (default `true`). List and detail responses also include read-only `username`.

**Membership plan.** `name`, `plan_type` (`monthly`, `quarterly`, or `yearly`), `duration_days`, `price`, optional `description`, `is_active` (default `true`), and `created_at`.

**Membership.** `member`, `plan`, `start_date`, `end_date`, and `status` (`active`, `expired`, or `cancelled`; default `active`). Responses also include read-only `member_name` and `plan_name`. Deleting a plan that still has memberships is blocked.

**Payment.** `membership`, `amount`, `payment_method` (`cash`, `upi`, `card`, or `online`), `payment_status` (`pending`, `completed`, or `failed`; default `pending`), optional unique `transaction_id`, and `payment_date`. Responses also include read-only `member_name`. Deleting a membership that still has payments is blocked.

## Example

Create a trainer after you have an access token:

```bash
curl -X POST http://127.0.0.1:8000/api/trainers/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jordan Lee",
    "email": "jordan@example.com",
    "phone": "5550100",
    "specialization": "Strength",
    "experience": 6
  }'
```

Create a member linked to an existing user. `trainer` can be omitted.

```bash
curl -X POST http://127.0.0.1:8000/api/members/ \
  -H "Authorization: Bearer <access>" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "trainer": 1,
    "phone": "5550199",
    "age": 28
  }'
```
For api use 

1. Register User
POST
http://127.0.0.1:8000/api/register/


Body → raw → JSON
{
    "username": "sarah",
    "email": "sarah@gmail.com",
    "password": "Sarah@12345"
}


2. Login – Get Token
POST
http://127.0.0.1:8000/api/token/


{
    "username": "sarah",
    "password": "Sarah@12345"
}


Copy the access token.
3. Create Trainer
POST
http://127.0.0.1:8000/api/trainers/


Authorization → Bearer Token → Sarah's access token.
{
    "full_name": "Michael Anderson",
    "email": "michael@gmail.com",
    "phone": "9876543211",
    "specialization": "Cardio and Fitness",
    "experience": 8,
    "is_active": true
}


4. Create Member
POST
http://127.0.0.1:8000/api/members/


{
    "user": 3,
    "trainer": 2,
    "phone": "9876543212",
    "age": 26,
    "joined_date": "2026-11-10",
    "is_active": true
}


5. Create Membership Plan
POST
http://127.0.0.1:8000/api/plans/


{
    "name": "Platinum Quarterly",
    "plan_type": "quarterly",
    "duration_days": 90,
    "price": "4000.00",
    "description": "Premium gym access for three months",
    "is_active": true
}


6. Create Membership
POST
http://127.0.0.1:8000/api/memberships/


{
    "member": 2,
    "plan": 2,
    "start_date": "2026-11-10",
    "end_date": "2027-02-08",
    "status": "active"
}


7. Create Payment
POST
http://127.0.0.1:8000/api/payments/


{
    "membership": 2,
    "amount": "4000.00",
    "payment_method": "card",
    "payment_status": "completed",
    "transaction_id": "TXN20261110002",
    "payment_date": "2026-11-10"
}



8. Complete GET URLs
GET http://127.0.0.1:8000/api/trainers/

GET http://127.0.0.1:8000/api/trainers/2/

GET http://127.0.0.1:8000/api/members/

GET http://127.0.0.1:8000/api/members/2/

GET http://127.0.0.1:8000/api/plans/

GET http://127.0.0.1:8000/api/plans/2/

GET http://127.0.0.1:8000/api/memberships/

GET http://127.0.0.1:8000/api/memberships/2/

GET http://127.0.0.1:8000/api/payments/

GET http://127.0.0.1:8000/api/payments/2/