---
phase: 22-go-java-kotlin-language-packs
plan: "02"
subsystem: packs
tags: [java, language-pack, tdd]
dependency_graph:
  requires: ["22-01"]
  provides: ["argus/packs/java/"]
  affects: ["argus packs list", "argus packs show java", "argus generate"]
tech_stack:
  added: []
  patterns: [isolation-config-constant, tdd-red-green]
key_files:
  created:
    - argus/packs/java/pack.yml
    - argus/packs/java/instructions.md
    - argus/packs/java/checklist.md
    - argus/packs/java/examples.md
  modified:
    - tests/integration/test_generate.py
key_decisions:
  - "Optional.orElseThrow chosen as key test phrase — lives in instructions.md Null Discipline section, stable and unique"
  - "JAVA_CONFIG isolation constant follows GO_CONFIG and prior pack precedents"
  - "Java pack is framework-agnostic — FORBIDDEN: Spring, Jakarta EE, Quarkus, Hibernate"
  - "Java version gating annotated inline: (Java 21+) for pattern matching switch, (Java 22+) for unnamed patterns"
metrics:
  duration: "2 min"
  completed: "2026-06-25"
  tasks: 2
  files: 5
---

# Phase 22 Plan 02: Java Language Pack Summary

Java 17+ language pack injecting modern-types, null-discipline, OOP-discipline, and exception-handling rules via `Optional.orElseThrow` key phrase, following established isolation-config-constant TDD pattern.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add failing JAVA_CONFIG and three java tests (RED) | 381218a | tests/integration/test_generate.py |
| 2 | Author four java pack files (GREEN) | 7e9b7f4 | argus/packs/java/{pack.yml,instructions.md,checklist.md,examples.md} |

## Decisions Made

- `Optional.orElseThrow` chosen as key test phrase — lives in `instructions.md` Null Discipline section, stable and unique
- `JAVA_CONFIG` isolation constant follows `GO_CONFIG` and prior pack precedents
- Java pack is framework-agnostic — FORBIDDEN: Spring, Jakarta EE, Quarkus, Hibernate
- Java version gating annotated inline: `(Java 21+)` for pattern matching switch, `(Java 22+)` for unnamed patterns

## Verification

- `argus packs list` includes `java`
- `argus packs show java` renders `Optional.orElseThrow`
- `generate` with java+claude config writes `Optional.orElseThrow` into `.claude/rules/java.md`
- Full suite: 34 passed, 80.2% coverage (green gate)
- No framework leakage: grep for spring/jakarta/quarkus/hibernate returns nothing

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check: PASSED
