# Testcontainers Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `testcontainers` pack to `argus/packs/` covering when to use real Docker containers for integration tests and how to configure lifecycle, wait strategies, and state reset correctly across Python, Java, and Go.

**Architecture:** Four new files under `argus/packs/testcontainers/` (pack.yml, instructions.md, checklist.md, examples.md) added to the pack registry in `tests/test_packs.py` and `.argus.yml`, then regenerated into `.claude/rules/` and `.claude/skills/` via `argus generate`.

**Tech Stack:** Python (testcontainers-python / pytest), Java (Testcontainers Java + JUnit 5), Go (testcontainers-go). No new runtime dependencies — examples reference each language's official testcontainers library.

## Global Constraints

- `category` must be one of: `workflow`, `architecture`, `quality`, `process` (enforced by `test_pack_yml_is_valid`)
- `platforms` field must be a list (enforced by the same test)
- `instructions.md` must have more than 100 characters after stripping whitespace
- Pack `name` in `pack.yml` must equal the directory name `testcontainers`
- Run `uv run pytest tests/ -v` to execute the test suite
- Run `uv run argus generate` to regenerate platform files after updating `.argus.yml`

---

### Task 1: Write failing tests for the testcontainers pack

**Files:**
- Modify: `tests/test_packs.py:7` (the `REQUIRED_PACKS` list)

**Interfaces:**
- Produces: 5 failing parametrized test cases (one per test function, for the `testcontainers` parameter)

- [ ] **Step 1: Add `testcontainers` to `REQUIRED_PACKS` in `tests/test_packs.py`**

Change line 7 from:
```python
REQUIRED_PACKS = ["atomic-commit", "tdd", "solid", "code-quality", "pre-commit", "type-safety", "error-handling", "documentation-standards", "dependency-injection", "design-patterns", "refactoring", "testing-strategy"]
```
To:
```python
REQUIRED_PACKS = ["atomic-commit", "tdd", "solid", "code-quality", "pre-commit", "type-safety", "error-handling", "documentation-standards", "dependency-injection", "design-patterns", "refactoring", "testing-strategy", "testcontainers"]
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
uv run pytest tests/test_packs.py -v -k testcontainers
```

Expected output — 5 failures:
```
FAILED tests/test_packs.py::test_pack_directory_exists[testcontainers]
FAILED tests/test_packs.py::test_pack_has_pack_yml[testcontainers]
FAILED tests/test_packs.py::test_pack_yml_is_valid[testcontainers]
FAILED tests/test_packs.py::test_pack_has_instructions[testcontainers]
FAILED tests/test_packs.py::test_pack_name_matches_directory[testcontainers]
```

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_packs.py
git commit -m "test: add failing tests for testcontainers pack"
```

---

### Task 2: Create the four pack files

**Files:**
- Create: `argus/packs/testcontainers/pack.yml`
- Create: `argus/packs/testcontainers/instructions.md`
- Create: `argus/packs/testcontainers/checklist.md`
- Create: `argus/packs/testcontainers/examples.md`

**Interfaces:**
- Consumes: `Pack` dataclass from `argus/adapters/base.py` — fields `name`, `manifest`, `instructions`, `checklist`, `examples`
- Produces: a loadable pack named `testcontainers` with `category: quality` and `requires: [testing-strategy]`

- [ ] **Step 1: Create `argus/packs/testcontainers/pack.yml`**

```yaml
name: testcontainers
description: Use real containers for integration tests — lifecycle, wait strategies, and when to reach for a fake instead
category: quality
requires:
  - testing-strategy
platforms: [all]
```

- [ ] **Step 2: Create `argus/packs/testcontainers/instructions.md`**

```markdown
# Testcontainers

## Core Rule
Use Testcontainers only when the behavior under test depends on the real service's semantics —
SQL constraints, index behavior, Redis TTL eviction, Kafka partition assignment. If an in-memory
fake gives equal confidence, use the fake: it starts in microseconds and has no Docker dependency.

## When to Use Containers

| Scenario | Use |
|---|---|
| DB constraint / migration correctness | Testcontainers |
| Kafka partition / consumer group semantics | Testcontainers |
| Redis TTL / eviction / pub-sub | Testcontainers |
| Simple CRUD (no constraint logic) | In-memory fake |
| External HTTP API call | HTTP stub (e.g., WireMock / responses) |
| Queue enqueue/dequeue abstraction | Fake implementation |

## Container Lifecycle

Containers are expensive to start (1–10 seconds each). Default to **session scope** — one
container per test run, shared across all tests that need it. Use **function scope** only when
tests corrupt shared state in a way that cannot be reset (e.g., schema migrations mid-run).

Reset state between tests by truncating tables or flushing keys — do not restart the container.

## Wait Strategies

Never assume a container is ready when Docker reports it started. Always configure a wait
strategy before the first query:

- **Postgres / MySQL:** wait for port + log line ("database system is ready to accept connections")
- **Redis:** wait for listening port
- **Kafka:** wait for log line or topic availability

Never use `time.sleep` as a wait strategy — it either waits too long or fails intermittently.

## CI Requirements

Testcontainers requires a Docker daemon accessible to the test runner. Ensure your CI environment
has Docker-in-Docker (DinD) or a mounted Docker socket. If Docker is unavailable, the test suite
must fail fast with a clear error — not silently skip integration tests.

## Red Flags — Stop and Correct
- Container created and destroyed per test function (use session or class scope instead)
- `time.sleep` used instead of a wait strategy or health check
- `testcontainers` imported in production (non-test) code
- Testcontainers used for simple CRUD with no DB-specific semantics (use an in-memory fake)
- Container restarted between tests to reset state (truncate or flush instead)
```

- [ ] **Step 3: Create `argus/packs/testcontainers/checklist.md`**

```markdown
## Testcontainers Pre-Commit Checklist

- [ ] Container used only where real service semantics are required — not for simple CRUD
- [ ] Container is session or class scoped — not created and destroyed per test function
- [ ] Wait strategy or health check configured before the first query
- [ ] No `testcontainers` import appears in production (non-test) code
- [ ] State reset between tests via truncate or flush — container not restarted
- [ ] CI runner has Docker available and fails fast with a clear error if it does not
```

- [ ] **Step 4: Create `argus/packs/testcontainers/examples.md`**

````markdown
## Testcontainers Examples

### Python (testcontainers-python + pytest)

#### Correct — Session-scoped fixtures in `conftest.py`

```python
# tests/conftest.py
import pytest
import psycopg2
import redis as redis_client
from kafka import KafkaProducer
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
    conn = psycopg2.connect(postgres_container.get_connection_url())
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

    redisContainer, err := redis.RunContainer(ctx, testcontainers.WithImage("redis:7"))
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
````

- [ ] **Step 5: Run all tests to confirm they pass**

```bash
uv run pytest tests/test_packs.py -v -k testcontainers
```

Expected output — 5 passes:
```
PASSED tests/test_packs.py::test_pack_directory_exists[testcontainers]
PASSED tests/test_packs.py::test_pack_has_pack_yml[testcontainers]
PASSED tests/test_packs.py::test_pack_yml_is_valid[testcontainers]
PASSED tests/test_packs.py::test_pack_has_instructions[testcontainers]
PASSED tests/test_packs.py::test_pack_name_matches_directory[testcontainers]
```

Then run the full suite to confirm nothing else broke:
```bash
uv run pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit the pack files**

```bash
git add argus/packs/testcontainers/
git commit -m "feat: add testcontainers pack with lifecycle and wait-strategy rules"
```

---

### Task 3: Register testcontainers in `.argus.yml` and regenerate platform files

**Files:**
- Modify: `.argus.yml` (add `testcontainers` to `packs` list)
- Generated (written by `argus generate`): `.claude/rules/testcontainers.md`, `.claude/skills/testcontainers/SKILL.md`
- Generated (updated by `argus generate`): `CLAUDE.md`, `AGENTS.md`, and equivalents for opencode, copilot, cursor

**Interfaces:**
- Consumes: `argus/packs/testcontainers/` files created in Task 2
- Produces: `testcontainers` rule and skill available to all configured AI platforms

- [ ] **Step 1: Add `testcontainers` to the `packs` list in `.argus.yml`**

Change `.argus.yml` from:
```yaml
packs:
- atomic-commit
- tdd
- solid
- code-quality
- pre-commit
- type-safety
- error-handling
- documentation-standards
- dependency-injection
- design-patterns
- refactoring
- testing-strategy
platforms:
- claude
- opencode
- copilot
- cursor
```

To:
```yaml
packs:
- atomic-commit
- tdd
- solid
- code-quality
- pre-commit
- type-safety
- error-handling
- documentation-standards
- dependency-injection
- design-patterns
- refactoring
- testing-strategy
- testcontainers
platforms:
- claude
- opencode
- copilot
- cursor
```

- [ ] **Step 2: Run `argus generate` to write the platform files**

```bash
uv run argus generate
```

Expected output includes:
```
  ✓ CLAUDE.md
  ✓ .claude/rules/testcontainers.md
  ✓ .claude/skills/testcontainers/SKILL.md
  ✓ AGENTS.md
  ...
```

- [ ] **Step 3: Verify the generated files exist and contain the right content**

```bash
grep "Testcontainers" .claude/rules/testcontainers.md | head -3
grep "Testcontainers Pre-Commit" .claude/skills/testcontainers/SKILL.md
```

Expected:
- `.claude/rules/testcontainers.md` contains "# Testcontainers"
- `.claude/skills/testcontainers/SKILL.md` contains "## Testcontainers Pre-Commit Checklist"

- [ ] **Step 4: Run the full test suite one final time**

```bash
uv run pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the config change and all generated files**

`argus generate` updates files for every configured platform (claude, opencode, copilot, cursor). Stage everything it touched:

```bash
git add .argus.yml
git add CLAUDE.md AGENTS.md .claude/rules/testcontainers.md .claude/skills/testcontainers/
git add GEMINI.md .cursor/ .opencode/ .github/copilot-instructions.md 2>/dev/null || true
git commit -m "feat: register testcontainers pack and regenerate platform files"
```
