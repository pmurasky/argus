## Kotlin Examples

### Null Safety — Safe Call vs Bang Operator

**Avoid**
```kotlin
val length = name!!.length
```

**Prefer**
```kotlin
val nonNullName = requireNotNull(name) { "name must not be null" }
val length = nonNullName.length
```

### Multi-Branch Logic — when vs if/else

**Avoid**
```kotlin
if (status == "active") {
    activate(user)
} else if (status == "suspended") {
    suspend(user)
} else if (status == "deleted") {
    delete(user)
} else {
    throw IllegalArgumentException("Unknown status: $status")
}
```

**Prefer**
```kotlin
when (status) {
    "active"    -> activate(user)
    "suspended" -> suspend(user)
    "deleted"   -> delete(user)
    else        -> throw IllegalArgumentException("Unknown status: $status")
}
```

### Coroutine Scope — Structured vs GlobalScope

**Avoid**
```kotlin
GlobalScope.launch {
    fetchData()
}
```

**Prefer**
```kotlin
viewModelScope.launch {
    fetchData()
}
```

### String Building — Template vs Concatenation

**Avoid**
```kotlin
val message = "Hello, " + name + "! You have " + count + " messages."
```

**Prefer**
```kotlin
val message = "Hello, $name! You have $count messages."
```
