# Frontend Tests

## Running Tests

```bash
# Unit & integration tests
npm test

# E2E tests (requires dev server running)
npm run test:e2e

# With coverage
npm run test:coverage
```

## Structure

- `unit/` - Component, service, and store tests (Vitest)
- `integration/` - API integration tests (Vitest) 
- `e2e/` - End-to-end user workflows (Playwright)

## Notes

- E2E tests require `npm run dev` to be running first
- Use `data-test` attributes for element selection in tests 