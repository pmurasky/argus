# Spring

## IoC Container & Stereotypes
- Constructor-inject all collaborators; never field-inject with `@Autowired` on fields
- Use `@Component` for generic beans, `@Service` for application/business logic, `@Repository` for persistence adapters — match the stereotype to the layer
- Mark a single constructor and omit `@Autowired` (Spring auto-wires the sole constructor)
- Declare bean wiring in `@Configuration` classes with `@Bean` methods; avoid component-scanning third-party classes
- Prefer `@ConfigurationProperties` typed beans over scattered `@Value` injection

## Data JPA
- Define entities with `@Entity`; map identity with `@Id` + `@GeneratedValue`
- Use `jakarta.persistence.*` imports (Spring 7 / Jakarta EE 11), never `javax.persistence.*`
- Extend `JpaRepository<Entity, IdType>` for repositories; declare derived query methods rather than hand-written JPQL where possible
- Annotate write operations with `@Transactional`; keep read paths non-transactional or `@Transactional(readOnly = true)`
- Avoid the N+1 query problem: use `@EntityGraph` or `join fetch` for needed associations
- Never expose entities directly from controllers — map to a response type at the boundary

## REST API Design
- Annotate controllers with `@RestController`; set the base path with `@RequestMapping` at the class level
- Use method-specific mappings: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`
- Bind path variables with `@PathVariable`, query params with `@RequestParam`, body with `@RequestBody`
- Return `ResponseEntity<T>` to control status codes; use `201 Created` on resource creation with a `Location` header
- Centralize error mapping with `@RestControllerAdvice` + `@ExceptionHandler`; never leak stack traces to clients
- Validate request bodies with `@Valid` and Jakarta Bean Validation annotations

## Testing (Spring Test Slices)
- Use `@SpringBootTest` only for full-context integration tests — it is the slowest slice
- Use `@WebMvcTest(Controller.class)` for controller-layer tests with `MockMvc`; load only the web layer
- Use `@DataJpaTest` for repository tests against an embedded/in-memory database; it rolls back per test
- Prefer the narrowest slice that covers the behavior — reserve `@SpringBootTest` for true end-to-end wiring
- Inject test collaborators via constructor in test classes just as in production code

## Red Flags — Stop and Correct
- `@Autowired` on a field instead of constructor injection
- `javax.persistence.*` or `javax.*` imports instead of `jakarta.*`
- JPA entity returned directly from a `@RestController` method
- `@SpringBootTest` used where `@WebMvcTest` or `@DataJpaTest` would suffice
- Business logic in a `@RestController` method instead of an injected `@Service`
- Missing `@Transactional` on a multi-write service method
