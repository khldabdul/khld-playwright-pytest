# Test Cases: ReqRes (API)

**URL**: https://reqres.in/  
**Type**: Quick Prototyping / Mocking  
**Priority**: 🥈 Second API to implement

---

## Test Suite: Users - Read

### TC-RR-001: List Users (Page 1)
- **Endpoint**: `GET /api/users?page=1`
- **Expected**: Status 200, `page: 1`, array of users

### TC-RR-002: List Users (Page 2)
- **Endpoint**: `GET /api/users?page=2`
- **Expected**: Status 200, `page: 2`, different users

### TC-RR-003: Get Single User
- **Endpoint**: `GET /api/users/2`
- **Expected**: Status 200, user with `id: 2`

### TC-RR-004: Get Non-Existent User
- **Endpoint**: `GET /api/users/23`
- **Expected**: Status 404, empty object `{}`

---

## Test Suite: Users - Create/Update/Delete

### TC-RR-010: Create User
- **Endpoint**: `POST /api/users`
- **Body**: `{"name": "morpheus", "job": "leader"}`
- **Expected**: Status 201, response includes `id`, `createdAt`

### TC-RR-011: Update User (PUT)
- **Endpoint**: `PUT /api/users/2`
- **Body**: `{"name": "morpheus", "job": "zion resident"}`
- **Expected**: Status 200, response includes `updatedAt`

### TC-RR-012: Update User (PATCH)
- **Endpoint**: `PATCH /api/users/2`
- **Body**: `{"name": "neo"}`
- **Expected**: Status 200

### TC-RR-013: Delete User
- **Endpoint**: `DELETE /api/users/2`
- **Expected**: Status 204, no content

---

## Test Suite: Authentication

### TC-RR-020: Login - Successful
- **Endpoint**: `POST /api/login`
- **Body**: `{"email": "eve.holt@reqres.in", "password": "cityslicka"}`
- **Expected**: Status 200, response contains `token`

### TC-RR-021: Login - Missing Password
- **Endpoint**: `POST /api/login`
- **Body**: `{"email": "peter@klaven"}`
- **Expected**: Status 400, `error: "Missing password"`

### TC-RR-022: Register - Successful
- **Endpoint**: `POST /api/register`
- **Body**: `{"email": "eve.holt@reqres.in", "password": "pistol"}`
- **Expected**: Status 200, response contains `id`, `token`

### TC-RR-023: Register - Missing Password
- **Endpoint**: `POST /api/register`
- **Body**: `{"email": "sydney@fife"}`
- **Expected**: Status 400, `error: "Missing password"`

---

## Test Suite: Resources

### TC-RR-030: List Resources
- **Endpoint**: `GET /api/unknown`
- **Expected**: Status 200, list of color resources

### TC-RR-031: Single Resource
- **Endpoint**: `GET /api/unknown/2`
- **Expected**: Status 200, resource with color data

### TC-RR-032: Resource Not Found
- **Endpoint**: `GET /api/unknown/23`
- **Expected**: Status 404

---

## Test Suite: Delayed Response

### TC-RR-040: Delayed Response
- **Endpoint**: `GET /api/users?delay=3`
- **Expected**: Status 200, response after ~3 seconds

---

## API Client Methods

| Method | Description |
|--------|-------------|
| `list_users(page)` | Get paginated users |
| `get_user(id)` | Get single user |
| `create_user(data)` | Create user |
| `update_user(id, data)` | Full update |
| `delete_user(id)` | Delete user |
| `login(email, password)` | Login |
| `register(email, password)` | Register |
