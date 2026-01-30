"""
ReqRes API Tests - Configuration Guide
=======================================

## ✅ WORKING - API Key Authentication

**Status:** OPERATIONAL  
**All 14 tests passing!**

### API Key Configuration

The ReqRes API uses a custom `x-api-key` header for authentication, which successfully bypasses Cloudflare bot protection.

**API Key:** `reqres_c3c7dc55078b4da5b6c83a939c8890ff`

### Setup

The API key is configured in `config/apps/reqres_config.yml`:

```yaml
extra_config:
  api_key: "reqres_c3c7dc55078b4da5b6c83a939c8890ff"
```

The client automatically adds the `x-api-key` header to all requests when the API key is provided.

### Running Tests

```bash
# Run all ReqRes tests
pytest apps/api/reqres/ -v

# Results: 14 passed in ~6 seconds
```

### Test Coverage

**All 14 tests passing:**

**Authentication** (4 tests):
- ✅ Register successful
- ✅ Register unsuccessful (validation)
- ✅ Login successful
- ✅ Login unsuccessful (validation)

**User Management** (7 tests):
- ✅ Get users list (paginated)
- ✅ Get single user by ID
- ✅ Get user not found (404)
- ✅ Create user
- ✅ Update user (PUT)
- ✅ Patch user (PATCH)
- ✅ Delete user

**Resources** (3 tests):
- ✅ Get resources list
- ✅ Get single resource
- ✅ Get resource not found (404)

### Solution Details

Originally facing `403 Forbidden` errors from Cloudflare bot protection. Fixed by:

1. Adding custom `x-api-key` header support to `ReqResClient`
2. Configuring API key in YAML config
3. Handling double-nested config structure in conftest

**Credit:** Solution discovered through user suggestion to test with curl using custom header!

```bash
# This worked:
curl -H "x-api-key: reqres_c3c7dc55078b4da5b6c83a939c8890ff" "https://reqres.in/api/users?page=2"
```
"""
