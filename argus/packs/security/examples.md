## Security Examples

### Injection — SQL

**Vulnerable**
```python
query = f"SELECT * FROM users WHERE name = '{user_input}'"
db.execute(query)
```

**Secure**
```python
db.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

### Injection — Shell

**Vulnerable**
```python
subprocess.run(f"convert {filename} output.png", shell=True)
```

**Secure**
```python
subprocess.run(["convert", filename, "output.png"])
```

### Cryptographic Failures

**Vulnerable**
```python
SECRET_KEY = "my-hardcoded-key"
password_hash = hashlib.md5(password.encode()).hexdigest()
```

**Secure**
```python
SECRET_KEY = os.environ["SECRET_KEY"]
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Input Validation

**Vulnerable**
```python
def create_user(data: dict) -> None:
    db.insert("users", data)  # no validation
```

**Secure**
```python
def create_user(data: dict) -> None:
    if not isinstance(data.get("email"), str) or len(data["email"]) > 254:
        raise ValidationError("Invalid email")
    if not EMAIL_RE.match(data["email"]):
        raise ValidationError("Invalid email format")
    db.insert("users", data)
```
