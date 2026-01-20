# Test Cases: Petstore Swagger (API)

**URL**: https://petstore.swagger.io/v2  
**Docs**: https://petstore.swagger.io/  
**Type**: OpenAPI/Swagger Spec  
**Priority**: 🥉 Third API to implement

---

## Note

⚠️ Public instance can be flaky due to high usage. Tests should be resilient.

---

## Test Suite: Pet Operations

### TC-PS-001: Add New Pet
- **Endpoint**: `POST /pet`
- **Body**:
  ```json
  {
    "id": 12345,
    "name": "doggie",
    "category": {"id": 1, "name": "Dogs"},
    "photoUrls": ["string"],
    "tags": [{"id": 0, "name": "string"}],
    "status": "available"
  }
  ```
- **Expected**: Status 200, pet created

### TC-PS-002: Get Pet by ID
- **Endpoint**: `GET /pet/{petId}`
- **Expected**: Status 200, pet object

### TC-PS-003: Get Pet - Not Found
- **Endpoint**: `GET /pet/99999999`
- **Expected**: Status 404

### TC-PS-004: Update Pet
- **Endpoint**: `PUT /pet`
- **Body**: Updated pet object
- **Expected**: Status 200, pet updated

### TC-PS-005: Delete Pet
- **Endpoint**: `DELETE /pet/{petId}`
- **Headers**: `api_key: special-key`
- **Expected**: Status 200

### TC-PS-006: Find Pets by Status
- **Endpoint**: `GET /pet/findByStatus?status=available`
- **Expected**: Status 200, array of available pets

### TC-PS-007: Find Pets by Tags
- **Endpoint**: `GET /pet/findByTags?tags=tag1,tag2`
- **Expected**: Status 200, filtered pets (deprecated)

---

## Test Suite: Store Operations

### TC-PS-020: Get Inventory
- **Endpoint**: `GET /store/inventory`
- **Expected**: Status 200, inventory counts by status

### TC-PS-021: Place Order
- **Endpoint**: `POST /store/order`
- **Body**:
  ```json
  {
    "id": 1,
    "petId": 12345,
    "quantity": 1,
    "shipDate": "2025-01-01T00:00:00.000Z",
    "status": "placed",
    "complete": true
  }
  ```
- **Expected**: Status 200, order created

### TC-PS-022: Get Order by ID
- **Endpoint**: `GET /store/order/{orderId}`
- **Expected**: Status 200, order object

### TC-PS-023: Delete Order
- **Endpoint**: `DELETE /store/order/{orderId}`
- **Expected**: Status 200

---

## Test Suite: User Operations

### TC-PS-030: Create User
- **Endpoint**: `POST /user`
- **Body**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "password": "password123",
    "phone": "1234567890",
    "userStatus": 1
  }
  ```
- **Expected**: Status 200

### TC-PS-031: Get User by Username
- **Endpoint**: `GET /user/{username}`
- **Expected**: Status 200, user object

### TC-PS-032: Login User
- **Endpoint**: `GET /user/login?username=testuser&password=password123`
- **Expected**: Status 200, session token in header

### TC-PS-033: Logout User
- **Endpoint**: `GET /user/logout`
- **Expected**: Status 200

### TC-PS-034: Update User
- **Endpoint**: `PUT /user/{username}`
- **Body**: Updated user object
- **Expected**: Status 200

### TC-PS-035: Delete User
- **Endpoint**: `DELETE /user/{username}`
- **Expected**: Status 200

---

## Test Suite: File Upload

### TC-PS-040: Upload Pet Image
- **Endpoint**: `POST /pet/{petId}/uploadImage`
- **Content-Type**: `multipart/form-data`
- **Body**: Image file
- **Expected**: Status 200, upload successful

---

## API Client Methods

| Method | Description |
|--------|-------------|
| `add_pet(data)` | Create pet |
| `get_pet(id)` | Get pet |
| `update_pet(data)` | Update pet |
| `delete_pet(id)` | Delete pet |
| `find_by_status(status)` | Find pets by status |
| `get_inventory()` | Store inventory |
| `place_order(data)` | Place order |
| `create_user(data)` | Create user |
| `login(username, password)` | User login |
| `upload_image(pet_id, file)` | Upload image |
