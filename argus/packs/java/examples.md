## Java Examples

### Immutable Data Carrier

**Avoid**
```java
public class Point {
    private int x;
    private int y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int getX() { return x; }
    public int getY() { return y; }
}
```

**Prefer**
```java
public record Point(int x, int y) {}
```

### Absent Value

**Avoid**
```java
public User findById(long id) {
    User user = db.query(id);
    return user; // may return null
}

// caller
User u = repo.findById(42);
String name = u.getName(); // NullPointerException if absent
```

**Prefer**
```java
public Optional<User> findById(long id) {
    return Optional.ofNullable(db.query(id));
}

// caller
String name = repo.findById(42)
    .map(User::getName)
    .orElseThrow(() -> new UserNotFoundError(42));
```

### Exception Handling

**Avoid**
```java
try {
    processOrder(order);
} catch (Exception e) {
    log.error("Failed", e);
}
```

**Prefer**
```java
try {
    processOrder(order);
} catch (OrderValidationError e) {
    log.warn("Invalid order {}: {}", order.id(), e.getMessage());
} catch (PaymentGatewayError e) {
    throw new OrderProcessingError("Payment failed for order " + order.id(), e);
}
```

### Sealed Class and Switch Expression

**Avoid**
```java
// Open hierarchy — new subtypes silently fall through
if (shape instanceof Circle c) {
    return Math.PI * c.radius() * c.radius();
} else if (shape instanceof Rectangle r) {
    return r.width() * r.height();
}
```

**Prefer**
```java
// Java 21+
public sealed interface Shape permits Circle, Rectangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}

double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
};
```
