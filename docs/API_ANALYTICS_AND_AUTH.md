# API — Analytics & Authentication

## Base
- Backend base URL: `http://127.0.0.1:8000/api/`

> Auth is session-based (login creates a session cookie). Frontend uses CSRF + cookies.

---

## Authentication

### Login
- **POST** `/auth/login/`
- **Body**:
```json
{
  "username": "admin", 
  "password": "password123"
}
```
- `username` can be **username OR email**.

### Logout
- **POST** `/auth/logout/`

### Current user
- **GET** `/auth/me/`

### Password reset (request)
- **POST** `/auth/password-reset/request/`
- **Body**:
```json
{
  "email": "user@example.com"
}
```
- Always returns **200** (prevents email enumeration).
- Sends an email containing a link like:
`{FRONTEND_BASE_URL}/reset-password?token=...`

### Password reset (confirm)
- **POST** `/auth/password-reset/confirm/`
- **Body**:
```json
{
  "token": "<raw-token>",
  "new_password": "newpass123",
  "new_password_confirm": "newpass123"
}
```
- Returns **400** if token is invalid/expired.

---

## Analytics

### Summary (MVP)
- **GET** `/analytics/summary/`

### Advanced (all-in)
- **GET** `/analytics/advanced/`
- Query params:
  - `start=YYYY-MM-DD`
  - `end=YYYY-MM-DD`

Optional assumptions (query params):
- `fuel_price_per_liter` (default `1.5`)
- `driver_cost_per_hour` (default `8.0`)
- `vehicle_cost_per_km` (default `0.3`)
- `cap_shipments_per_vehicle_per_day` (default `30`)
- `cap_shipments_per_driver_per_day` (default `25`)
- `working_days_per_month` (default `22`)

Returns (high level):
- `shipments`: totals, growth, delivered/failed/delayed, rates, series, forecast
- `revenue`: totals, growth, series, forecast
- `routes`: totals, growth, series, forecast
- `fuel`: total liters, L/100km, series, forecast
- `incidents`: totals, growth, series, forecast, by_zone
- `profitability`: estimated costs/margins + by_service_type
- `staffing`: forecast of required vehicles/drivers
- `zones`: top_by_shipments, top_by_incidents
- `map`: destination_points (requires Destination lat/lng)

---

## Verification checklist (local)

### Setup
- Run migrations:
  - `python manage.py migrate`
- Install frontend deps:
  - `npm install`

### Test suite
- Run backend tests:
  - `python manage.py test core`

### Manual sanity
- Login in UI
- Open `/analytics` and confirm:
  - KPIs render
  - shipments/revenue/fuel/incidents charts render
  - zones + staffing + profitability tables render
  - map renders when destinations have lat/lng
- Password reset:
  - request reset email
  - copy link from backend console/email
  - confirm reset, login with new password
