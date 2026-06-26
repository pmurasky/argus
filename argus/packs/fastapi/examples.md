## FastAPI Examples

### Blocking I/O in async handler

**Avoid**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # blocks the event loop — starves all concurrent requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()
```

**Prefer**
```python
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, client: httpx.AsyncClient = Depends(get_http_client)):
    response = await client.get(f"https://api.example.com/users/{user_id}")
    return response.json()
```

### Router organization

**Avoid**
```python
# main.py — all routes inlined, no prefix/tags per route
@app.get("/users/")
async def list_users(): ...

@app.post("/users/")
async def create_user(): ...

@app.get("/orders/")
async def list_orders(): ...
```

**Prefer**
```python
# routers/users.py
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(service: UserService = Depends(get_user_service)): ...

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(body: UserCreate, service: UserService = Depends(get_user_service)): ...

# main.py
app.include_router(users.router)
app.include_router(orders.router)
```

### Service constructed in route body

**Avoid**
```python
@router.post("/orders/", response_model=OrderResponse)
async def create_order(body: OrderCreate):
    db = SessionLocal()          # connection leaked if handler raises
    service = OrderService(db)   # tight coupling, untestable
    return service.create(body)
```

**Prefer**
```python
@router.post("/orders/", response_model=OrderResponse, status_code=201)
async def create_order(body: OrderCreate, service: OrderService = Depends(get_order_service)):
    return await service.create(body)
```

### Pydantic v1 validator vs v2 field_validator

**Avoid**
```python
class UserCreate(BaseModel):
    class Config:
        orm_mode = True

    @validator("email")
    def email_must_be_lowercase(cls, v):
        return v.lower()
```

**Prefer**
```python
class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @field_validator("email", mode="before")
    @classmethod
    def email_must_be_lowercase(cls, v: str) -> str:
        return v.lower()
```
