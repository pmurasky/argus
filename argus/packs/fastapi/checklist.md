## FastAPI Checklist

- [ ] Route handlers are declared `async def`
- [ ] No blocking I/O (requests, time.sleep, sync DB drivers) inside async handlers
- [ ] Request and response Pydantic models declared per endpoint
- [ ] `Field()` used for API-level validation constraints
- [ ] Pydantic v2 `model_config` / `model_validator` / `field_validator` used (no v1 `Config` class or `@validator`)
- [ ] Shared resources (DB sessions, current user) injected via `Depends()`
- [ ] No services or connections constructed inside route bodies
- [ ] One `APIRouter` per feature/domain; routes not inlined in `main.py`
- [ ] `prefix` and `tags` set at the `APIRouter` level, not per endpoint
- [ ] `response_model=` declared on every route
