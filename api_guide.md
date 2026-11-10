# How to call this API

Base URL while the server is running:

```text
http://127.0.0.1:8000
```

Start it from the project folder:

```bash
source venv/bin/activate
python manage.py runserver
```

Keep that terminal open. Run the `curl` commands below in a second terminal.

Every URL ends with `/`. A missing slash makes Django redirect the request and the call fails.

The access token lasts 30 minutes. The refresh token lasts 7 days.

## URLs

| What | Method | URL | Login required |
| --- | --- | --- | --- |
| Register | POST | `http://127.0.0.1:8000/api/register/` | No |
| Get tokens | POST | `http://127.0.0.1:8000/api/token/` | No |
| Refresh access token | POST | `http://127.0.0.1:8000/api/token/refresh/` | No |
| Trainers | GET, POST | `http://127.0.0.1:8000/api/trainers/` | Yes |
| One trainer | GET, PUT, PATCH, DELETE | `http://127.0.0.1:8000/api/trainers/1/` | Yes |
| Members | GET, POST | `http://127.0.0.1:8000/api/members/` | Yes |
| One member | GET, PUT, PATCH, DELETE | `http://127.0.0.1:8000/api/members/1/` | Yes |
| Plans | GET, POST | `http://127.0.0.1:8000/api/plans/` | Yes |
| One plan | GET, PUT, PATCH, DELETE | `http://127.0.0.1:8000/api/plans/1/` | Yes |
| Memberships | GET, POST | `http://127.0.0.1:8000/api/memberships/` | Yes |
| One membership | GET, PUT, PATCH, DELETE | `http://127.0.0.1:8000/api/memberships/1/` | Yes |
| Payments | GET, POST | `http://127.0.0.1:8000/api/payments/` | Yes |
| One payment | GET, PUT, PATCH, DELETE | `http://127.0.0.1:8000/api/payments/1/` | Yes |
| Admin site | GET | `http://127.0.0.1:8000/admin/` | Superuser |

Replace `1` with the `id` from the create response. List is `GET` on the collection URL. Create is `POST` on that same URL. Read one row with `GET`, change some fields with `PATCH`, replace the row with `PUT`, and remove it with `DELETE`.

Create things in this order, because later rows point at earlier ones:

1. Register a user and get a token.
2. Create a trainer.
3. Create a member for that user.
4. Create a plan.
5. Create a membership for that member and plan.
6. Create a payment for that membership.

## 1. Register

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alex",
    "email": "alex@example.com",
    "password": "GymPass123"
  }'
```

Password must be at least 8 characters. A successful response looks like this. It does not include the password or the user id:

```json
{
  "username": "alex",
  "email": "alex@example.com"
}
```

If `alex` already exists, pick another username.

## 2. Get a token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alex",
    "password": "GymPass123"
  }'
```

Copy the `access` value from the response:

```json
{
  "access": "eyJhbGciOi...",
  "refresh": "eyJhbGciOi..."
}
```

Save it in the terminal you will use for the next calls:

```bash
TOKEN="paste-the-access-value-here"
```

Every later request needs this header:

```text
Authorization: Bearer <access token>
```

When the access token expires, get a new one with the refresh token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "paste-the-refresh-value-here"
  }'
```

## 3. Create a trainer

```bash
curl -X POST http://127.0.0.1:8000/api/trainers/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jordan Lee",
    "email": "jordan@example.com",
    "phone": "5550100",
    "specialization": "Strength",
    "experience": 6
  }'
```

Required fields: `full_name`, `email`, `phone`, `specialization`, `experience`. `email` must be unique. `is_active` defaults to `true`. The response includes `id`. Use that id as `trainer` on the member.

List trainers:

```bash
curl http://127.0.0.1:8000/api/trainers/ \
  -H "Authorization: Bearer $TOKEN"
```

Read trainer 1:

```bash
curl http://127.0.0.1:8000/api/trainers/1/ \
  -H "Authorization: Bearer $TOKEN"
```

Change one field:

```bash
curl -X PATCH http://127.0.0.1:8000/api/trainers/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"specialization": "Cardio"}'
```

## 4. Create a member

A member must point at an existing user. Registration does not return that id. Look it up:

```bash
./venv/bin/python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.get(username='alex').id)"
```

Then create the member. Put the printed number in `user`, and the trainer `id` in `trainer`. `trainer` can be left out.

```bash
curl -X POST http://127.0.0.1:8000/api/members/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "trainer": 1,
    "phone": "5550199",
    "age": 28
  }'
```

Required fields: `user`, `phone`, `age`. Each user can have only one member profile. The response adds read-only `username` and `joined_date`.

## 5. Create a plan

`plan_type` must be exactly `monthly`, `quarterly`, or `yearly`.

```bash
curl -X POST http://127.0.0.1:8000/api/plans/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly Basic",
    "plan_type": "monthly",
    "duration_days": 30,
    "price": "49.99",
    "description": "Gym floor access"
  }'
```

Required fields: `name`, `plan_type`, `duration_days`, `price`. `description` is optional.

## 6. Create a membership

`member` is the member id from step 4. `plan` is the plan id from step 5. Dates are `YYYY-MM-DD`.

`status` must be `active`, `expired`, or `cancelled`. If you omit it, the API stores `active`.

```bash
curl -X POST http://127.0.0.1:8000/api/memberships/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "member": 1,
    "plan": 1,
    "start_date": "2026-11-10",
    "end_date": "2026-12-10",
    "status": "active"
  }'
```

The response adds read-only `member_name` and `plan_name`.

## 7. Create a payment

`membership` is the membership id from step 6.

`payment_method` must be `cash`, `upi`, `card`, or `online`.

`payment_status` must be `pending`, `completed`, or `failed`. If you omit it, the API stores `pending`.

```bash
curl -X POST http://127.0.0.1:8000/api/payments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "membership": 1,
    "amount": "49.99",
    "payment_method": "upi",
    "payment_status": "completed",
    "transaction_id": "TXN-1001"
  }'
```

Required fields: `membership`, `amount`, `payment_method`. `transaction_id` is optional, and it must be unique when you send one. The response adds read-only `member_name` and `payment_date`.

List payments:

```bash
curl http://127.0.0.1:8000/api/payments/ \
  -H "Authorization: Bearer $TOKEN"
```

## Delete

Delete a payment before its membership, and delete a membership before its plan. The API blocks deleting a plan or membership that is still in use.

```bash
curl -X DELETE http://127.0.0.1:8000/api/payments/1/ \
  -H "Authorization: Bearer $TOKEN"
```

A successful delete returns an empty body and status `204`.

## If a call fails

| Status | Meaning |
| --- | --- |
| 401 | Missing or expired access token. Get a new one from `/api/token/` or `/api/token/refresh/`. |
| 400 | A field is missing, a choice is wrong, or an email, username, or `transaction_id` is already used. Read the JSON body. |
| 404 | That id does not exist, or the URL has no trailing `/`. |
