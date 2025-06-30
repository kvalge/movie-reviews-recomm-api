# Backend Tests

## Running Tests

```bash
pytest

pytest --cov=app --cov-report=html

pytest tests/test_routes/
```

## Structure

- `test_routes/` - API endpoint tests
- `test_services/` - Service layer tests  
- `test_models/` - Model tests
- `test_integration/` - Integration tests

## Notes

- Tests use in-memory SQLite database
- `conftest.py` provides common fixtures and test data 