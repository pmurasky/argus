## Python Examples

### String Interpolation

**Avoid**
```python
greeting = "Hello {}".format(name)
```

**Prefer**
```python
greeting = f"Hello {name}"
```

### Resource Management

**Avoid**
```python
f = open("data.txt")
data = f.read()
f.close()
```

**Prefer**
```python
with open("data.txt") as f:
    data = f.read()
```

### Filesystem Paths

**Avoid**
```python
import os
path = os.path.join(base, "sub", "file.txt")
```

**Prefer**
```python
from pathlib import Path
path = Path(base) / "sub" / "file.txt"
```

### Structured Data

**Avoid**
```python
user = {"name": "Ada", "age": 36}
```

**Prefer**
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```
