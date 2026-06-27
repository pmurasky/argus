## Testcontainers Examples

### Python (testcontainers-python + pytest)

#### Correct — Session-scoped fixtures in `conftest.py`

```python
# tests/conftest.py
import pytest
import psycopg2
import redis as redis_client
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16") as pg:
        yield pg


@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7") as r:
        yield r


@pytest.fixture(scope="session")
def kafka_container():
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as k:
        yield k


@pytest.fixture()
def pg_conn(postgres_container):
    conn = psycopg2.connect(
        host=postgres_container.get_container_host_ip(),
        port=postgres_container.get_exposed_port(5432),
        dbname=postgres_container.dbname,
        user=postgres_container.username,
        password=postgres_container.password,
    )
    yield conn
    with conn.cursor() as cur:
        cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
    conn.commit()
    conn.close()


@pytest.fixture()
def redis_conn(redis_container):
    r = redis_client.Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
    )
    yield r
    r.flushdb()


# Usage
def test_unique_email_constraint_enforced(pg_conn):
    # Given
    with pg_conn.cursor() as cur:
        cur.execute("INSERT INTO users (email) VALUES ('a@b.com')")
    pg_conn.commit()
    # When / Then
    with pytest.raises(psycopg2.errors.UniqueViolation):
        with pg_conn.cursor() as cur:
            cur.execute("INSERT INTO users (email) VALUES ('a@b.com')")
        pg_conn.commit()
```

#### Incorrect — Container created per test (5-second penalty per test)

```python
def test_unique_email_constraint_enforced():
    with PostgresContainer("postgres:16") as pg:  # starts a fresh container every test
        conn = psycopg2.connect(pg.get_connection_url())
        # ... test body
        conn.close()
```

---

### Java (Testcontainers Java + JUnit 5)

#### Correct — `static` `@Container` for class (shared) scope

```java
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.kafka.KafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;
import org.testcontainers.containers.wait.strategy.Wait;

@Testcontainers
class RepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
        .waitingFor(Wait.forLogMessage(".*database system is ready to accept connections.*", 1));

    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7")
        .withExposedPorts(6379)
        .waitingFor(Wait.forListeningPort());

    @Container
    static KafkaContainer kafka = new KafkaContainer(
        DockerImageName.parse("confluentinc/cp-kafka:7.6.0")
    );

    @BeforeEach
    void resetState() throws Exception {
        try (var conn = DriverManager.getConnection(postgres.getJdbcUrl(),
                postgres.getUsername(), postgres.getPassword());
             var stmt = conn.prepareStatement(
                "TRUNCATE users RESTART IDENTITY CASCADE")) {
            stmt.execute();
        }
    }

    @Test
    void uniqueEmailConstraintEnforced() {
        var repo = new UserRepository(postgres.getJdbcUrl(),
            postgres.getUsername(), postgres.getPassword());
        repo.save(new User("a@b.com"));

        assertThrows(DuplicateEmailException.class, () -> repo.save(new User("a@b.com")));
    }
}
```

#### Incorrect — Non-`static` `@Container` restarts the container before every test method

```java
@Testcontainers
class RepositoryIntegrationTest {
    @Container
    PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");
    // non-static: JUnit 5 creates a new instance per test, so the container
    // starts and stops around every single @Test method
}
```

---

### Go (testcontainers-go)

#### Correct — `TestMain` for session scope, `t.Cleanup` for state reset

```go
// tests/integration/main_test.go
package integration_test

import (
    "context"
    "database/sql"
    "errors"
    "fmt"
    "os"
    "testing"

    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    "github.com/testcontainers/testcontainers-go/modules/redis"
    "github.com/testcontainers/testcontainers-go/modules/kafka"
    "github.com/testcontainers/testcontainers-go/wait"
)

var (
    postgresURL string
    redisAddr   string
    kafkaBroker string
)

func TestMain(m *testing.M) {
    ctx := context.Background()

    pgContainer, err := postgres.RunContainer(ctx,
        testcontainers.WithImage("postgres:16"),
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready to accept connections"),
        ),
    )
    if err != nil {
        fmt.Fprintf(os.Stderr, "postgres container: %v\n", err)
        os.Exit(1)
    }
    defer pgContainer.Terminate(ctx)
    postgresURL, _ = pgContainer.ConnectionString(ctx, "sslmode=disable")

    redisContainer, err := redis.RunContainer(ctx,
        testcontainers.WithImage("redis:7"),
        testcontainers.WithWaitStrategy(wait.ForListeningPort()),
    )
    if err != nil {
        fmt.Fprintf(os.Stderr, "redis container: %v\n", err)
        os.Exit(1)
    }
    defer redisContainer.Terminate(ctx)
    redisAddr, _ = redisContainer.Endpoint(ctx, "")

    kafkaContainer, err := kafka.RunContainer(ctx,
        testcontainers.WithImage("confluentinc/cp-kafka:7.6.0"),
    )
    if err != nil {
        fmt.Fprintf(os.Stderr, "kafka container: %v\n", err)
        os.Exit(1)
    }
    defer kafkaContainer.Terminate(ctx)
    brokers, _ := kafkaContainer.Brokers(ctx)
    kafkaBroker = brokers[0]

    os.Exit(m.Run())
}

func TestUniqueEmailConstraintEnforced(t *testing.T) {
    db, err := sql.Open("pgx", postgresURL)
    if err != nil {
        t.Fatal(err)
    }
    t.Cleanup(func() {
        db.Exec("TRUNCATE users RESTART IDENTITY CASCADE")
        db.Close()
    })

    repo := NewUserRepository(db)
    if err := repo.Save(User{Email: "a@b.com"}); err != nil {
        t.Fatal(err)
    }

    err = repo.Save(User{Email: "a@b.com"})
    if !errors.Is(err, ErrDuplicateEmail) {
        t.Errorf("expected ErrDuplicateEmail, got %v", err)
    }
}
```

#### Incorrect — Container started inside each test function

```go
func TestUniqueEmailConstraintEnforced(t *testing.T) {
    ctx := context.Background()
    // New container per test — 5-10 second startup penalty every time
    pgContainer, _ := postgres.RunContainer(ctx, testcontainers.WithImage("postgres:16"))
    defer pgContainer.Terminate(ctx)
    // ... test body
}
```
