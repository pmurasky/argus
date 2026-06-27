# Testcontainers Pack Design

**Date:** 2026-06-26
**Status:** Approved

## Summary

Add a `testcontainers` pack to argus covering when to use real Docker containers for integration tests, how to manage container lifecycle correctly, and concrete patterns for Python, Java, and Go across Postgres, Redis, and Kafka.

## Problem

The existing `testing-strategy` pack mentions containerized infrastructure as a valid substitute for real services but gives no guidance on how to use it correctly. Teams make two recurring mistakes: reaching for Testcontainers when a faster in-memory fake would do, and creating per-test containers that slow the suite by 10–100×.

## Scope

Single pack at `argus/packs/testcontainers/` with four files: `pack.yml`, `instructions.md`, `checklist.md`, `examples.md`.

Not in scope: container orchestration beyond tests (Docker Compose for local dev, Kubernetes), service mesh or networking configuration, non-JVM Java frameworks.

## `pack.yml`

```yaml
name: testcontainers
description: Use real containers for integration tests — lifecycle, wait strategies, and when to reach for a fake instead
category: quality
requires:
  - testing-strategy
platforms: [all]
```

## `instructions.md` Sections

### Core Rule
Reach for Testcontainers only when the behavior under test depends on the real service's semantics — SQL constraints, index behavior, Redis TTL eviction, Kafka partition assignment. If an in-memory fake gives equal confidence, use the fake: it starts in microseconds and has no Docker dependency.

### Decision Table

| Scenario | Use |
|---|---|
| DB constraint / migration correctness | Testcontainers |
| Kafka partition / consumer group semantics | Testcontainers |
| Redis TTL / eviction / pub-sub | Testcontainers |
| Simple CRUD (no constraint logic) | In-memory fake |
| External HTTP API call | HTTP stub (e.g., WireMock / responses) |
| Queue enqueue/dequeue abstraction | Fake implementation |

### Container Lifecycle

Containers are expensive to start (1–10 seconds each). Default to **session scope** — one container per test run, shared across all tests that need it. Use **function scope** only when tests corrupt shared state in a way that cannot be reset (e.g., schema migrations mid-run).

Reset state between tests by truncating tables or flushing keys — do not restart the container.

### Wait Strategies

Never assume a container is ready when Docker reports it started. Always configure a wait strategy before the first query:

- **Postgres / MySQL:** wait for port + log line ("database system is ready")
- **Redis:** wait for port
- **Kafka:** wait for topic creation or log line

Never use `time.sleep` as a wait strategy.

### CI Requirements

Testcontainers requires a Docker daemon accessible to the test runner. Ensure your CI environment has Docker-in-Docker (DinD) or a Docker socket available. Document this requirement in your project's CI setup guide. If Docker is unavailable, the test suite must fail fast with a clear error — not silently skip integration tests.

## `checklist.md` Items

1. Container used only where real service semantics are required — not for simple CRUD
2. Container is session or class scoped — not created and destroyed per test function
3. Wait strategy or health check configured before the first query
4. No `testcontainers` import appears in production (non-test) code
5. State reset between tests (truncate/flush) without container restart
6. CI runner has Docker available and fails fast if it does not

## `examples.md` Structure

Three language sections, each with Postgres, Redis, and Kafka patterns. Each section shows:
- **Correct:** session-scoped container with proper wait strategy and state reset
- **Incorrect:** per-test container creation (no wait, no reuse)

### Python (testcontainers-python)
- pytest `conftest.py` session-scoped fixtures using `PostgresContainer`, `RedisContainer`, `KafkaContainer`
- `yield` fixture pattern for teardown
- Wrong: creating container inside a test function

### Java (Testcontainers Java + JUnit 5)
- `@Testcontainers` + `@Container` with `static` field for class-scoped reuse
- `PostgreSQLContainer`, `GenericContainer` (Redis), `KafkaContainer`
- Wrong: non-static `@Container` (restarts per test method)

### Go (testcontainers-go)
- `TestMain` or `testcontainers.GenericContainer` in `TestMain(m *testing.M)` for session scope
- `t.Cleanup` for teardown
- Wrong: container created inside `Test*` function

## Dependencies

- Requires `testing-strategy` pack (decision table extends the doubles guidance)
- No new tooling required — examples use each language's official testcontainers library
