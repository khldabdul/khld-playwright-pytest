# Test Cases: Restful Booker (API)

**URL**: https://restful-booker.herokuapp.com/  
**Docs**: https://restful-booker.herokuapp.com/apidoc/  
**Type**: CRUD + Token Authentication  
**Priority**: 🥇 First API to implement

---

## Authentication

Token required for PUT/PATCH/DELETE operations:

```json
POST /auth
{
  "username": "admin",
  "password": "password123"
}
```

---

## Test Suite: Health Check

### TC-RB-001: Ping Service
- **Endpoint**: `GET /ping`
- **Expected**: Status 201, text "Created"

---

## Test Suite: Authentication

### TC-RB-010: Create Token - Valid Credentials
- **Endpoint**: `POST /auth`
- **Body**: `{"username": "admin", "password": "password123"}`
- **Expected**: Status 200, response contains `token`

### TC-RB-011: Create Token - Invalid Credentials
- **Endpoint**: `POST /auth`
- **Body**: `{"username": "admin", "password": "wrong"}`
- **Expected**: Status 200, response contains `reason: "Bad credentials"`

---

## Test Suite: Booking CRUD

### TC-RB-020: Get All Booking IDs
- **Endpoint**: `GET /booking`
- **Expected**: Status 200, array of `{bookingid: number}`

### TC-RB-021: Get All Bookings with Filter
- **Endpoint**: `GET /booking?firstname=John&lastname=Smith`
- **Expected**: Status 200, filtered booking IDs

### TC-RB-022: Get Single Booking
- **Endpoint**: `GET /booking/:id`
- **Expected**: Status 200, full booking object

### TC-RB-023: Get Non-Existent Booking
- **Endpoint**: `GET /booking/999999`
- **Expected**: Status 404

### TC-RB-024: Create Booking
- **Endpoint**: `POST /booking`
- **Body**:
  ```json
  {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": true,
    "bookingdates": {
      "checkin": "2025-01-01",
      "checkout": "2025-01-05"
    },
    "additionalneeds": "Breakfast"
  }
  ```
- **Expected**: Status 200, booking created with ID

### TC-RB-025: Update Booking (PUT)
- **Endpoint**: `PUT /booking/:id`
- **Headers**: `Cookie: token=<abc123>`
- **Body**: Updated booking object
- **Expected**: Status 200, booking updated

### TC-RB-026: Partial Update Booking (PATCH)
- **Endpoint**: `PATCH /booking/:id`
- **Headers**: `Cookie: token=<abc123>`
- **Body**: `{"firstname": "James"}`
- **Expected**: Status 200, only firstname updated

### TC-RB-027: Delete Booking
- **Endpoint**: `DELETE /booking/:id`
- **Headers**: `Cookie: token=<abc123>`
- **Expected**: Status 201

### TC-RB-028: Update Without Token (401)
- **Endpoint**: `PUT /booking/:id` (no token)
- **Expected**: Status 403 Forbidden

---

## Test Suite: Full Lifecycle

### TC-RB-030: Complete Booking Lifecycle
- **Steps**:
  1. Create auth token
  2. Create new booking
  3. Verify booking exists (GET)
  4. Update booking (PUT)
  5. Verify update
  6. Delete booking
  7. Verify deletion (GET returns 404)
- **Expected**: All operations succeed in sequence

---

## API Client Methods

| Method | Description |
|--------|-------------|
| `create_token()` | Get auth token |
| `get_bookings()` | List all booking IDs |
| `get_booking(id)` | Get single booking |
| `create_booking(data)` | Create booking |
| `update_booking(id, data)` | Full update |
| `partial_update(id, data)` | Partial update |
| `delete_booking(id)` | Delete booking |
