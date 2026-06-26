# FastAPI

## Async Patterns
- Declare every route handler `async def` — FastAPI runs them on the event loop without blocking
- Use plain `def` ONLY for CPU-bound work; FastAPI offloads sync handlers to a thread pool
- Never call blocking I/O (requests, time.sleep, blocking DB drivers) inside an `async def` handler
- Use `async`-native libraries (httpx, asyncpg, databases) for I/O inside async handlers
- Stream large responses with `async for` and a generator rather than buffering in memory

## Pydantic Models
- Define a request model and a response model per endpoint as the typed I/O boundary
- Use Pydantic v2 syntax: `model_config`, `model_validator`, `field_validator` (never v1 `Config` class or `@validator`)
- Use `Field()` for API-level validation: `min_length`, `max_length`, `ge`/`le`, `description`, `alias`
- Set serialization behavior with `model_config = ConfigDict(populate_by_name=True, from_attributes=True)`
- Express cross-field rules with `@model_validator(mode="after")`, single-field rules with `@field_validator`
- Declare `response_model=` on the route so output is filtered and documented

## Dependency Injection
- Inject shared resources (DB sessions, current user, settings) with `Depends()`
- Write dependencies as functions or callables that `yield` for setup/teardown (e.g., DB session lifecycle)
- Depend on abstractions so tests override dependencies via `app.dependency_overrides`
- Never instantiate services or open connections inside a route body — inject them
- Layer dependencies: a higher-level dependency may itself declare `Depends()` on lower ones

## Router Organization
- Create one `APIRouter` per feature/domain; never inline all routes in `main.py`
- Set `prefix=` and `tags=[]` at the `APIRouter` level, not on individual endpoints
- Assemble the app by calling `app.include_router(...)` for each router in `main.py` / `app.py`
- Keep route handlers thin — delegate business logic to injected services
- Group request/response models with the router module they serve

## Red Flags — Stop and Correct
- Blocking I/O call inside an `async def` route handler
- Pydantic v1 `class Config:` or `@validator` instead of v2 `model_config` / `field_validator`
- Service or DB connection constructed inside a route body instead of injected with `Depends()`
- All routes defined directly on `app` in `main.py` instead of split into `APIRouter`s
- Endpoint without a declared `response_model` returning raw ORM objects
- `prefix`/`tags` repeated on every endpoint instead of set once at the router
