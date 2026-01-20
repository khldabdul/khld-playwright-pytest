"""
OMDb API Tests - Known Limitations and Configuration
=====================================================

## API Key Requirement

The OMDb API requires a valid API key to function. Tests will be skipped if the key is not configured.

### Setting the API Key

**Environment Variable:**
```bash
export OMDB_API_KEY=your_api_key_here
```

**Current API Key:** `264a1dae`

### Running OMDb Tests

```bash
# With API key
export OMDB_API_KEY=264a1dae
pytest apps/api/omdb/ -v

# Tests will auto-skip if key is not set
pytest apps/api/omdb/ -v  # Shows: "OMDb API key not configured"
```

## Test Coverage

All 5 tests passing:
- ✅ Search for existing movie
- ✅ Get movie by IMDb ID
- ✅ Get movie by title and year
- ✅ Search non-existent movie (error handling)
- ✅ Invalid ID handling

**Execution Time:** ~3 seconds
"""
