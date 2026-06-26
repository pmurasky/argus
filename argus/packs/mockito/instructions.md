# Mockito

## Setup
- Activate Mockito with `@ExtendWith(MockitoExtension.class)` (JUnit 5 and JUnit 6) — never the JUnit 4 `@RunWith(MockitoJUnitRunner.class)`
- Declare mocks as fields annotated `@Mock`; inject them into the subject with `@InjectMocks`
- Enable strict stubbing (Mockito 5 default) — remove unused stubs rather than relaxing strictness

## @Mock vs @Spy
- Use `@Mock` to replace a collaborator entirely — all methods return defaults until stubbed
- Use `@Spy` to wrap a real object and override only selected methods — the rest run real logic
- Stub a spy with `doReturn(...).when(spy).method()`, NOT `when(spy.method()).thenReturn(...)` (the latter calls the real method)
- Prefer `@Mock` by default; reach for `@Spy` only when partial real behavior is genuinely required

## Argument Captors
- Capture arguments passed to a mock with `ArgumentCaptor<T>` to assert on them after the fact
- Declare with `@Captor ArgumentCaptor<T> captor;` or `ArgumentCaptor.forClass(T.class)`
- Pass `captor.capture()` inside a `verify(...)` call, then assert on `captor.getValue()` / `getAllValues()`
- Use a captor only when you must inspect a complex argument — prefer `eq(...)` matchers for simple equality

## Verify Patterns
- Assert interactions with `verify(mock).method(args)`; assert count with `verify(mock, times(n))`
- Use `never()`, `atLeastOnce()`, `atMost(n)` for cardinality; `verifyNoInteractions(mock)` / `verifyNoMoreInteractions(mock)` to assert nothing else happened
- Match arguments with `eq()`, `any()`, `argThat(...)`; never mix raw values and matchers in one call
- Enforce call order across mocks with `InOrder inOrder = inOrder(a, b);` then `inOrder.verify(...)`

## Classic and BDD Style
- Classic stubbing: `when(mock.call()).thenReturn(value)` — still valid in Mockito 5, not deprecated
- BDD style (preferred for readability in given/when/then tests): `given(mock.call()).willReturn(value)` and `then(mock).should().call()` from `BDDMockito`
- Pick one style per test class and stay consistent — do not mix `when/verify` with `given/then`
- Stub voids with `doThrow(...)` / `doNothing().when(mock).voidCall()`

## Red Flags — Stop and Correct
- `@RunWith(MockitoJUnitRunner.class)` (JUnit 4 — replace with `@ExtendWith(MockitoExtension.class)`)
- `when(spy.method())` used to stub a `@Spy` (calls real method — use `doReturn().when(spy)`)
- Raw argument values mixed with matchers in the same `verify`/`when` call
- Captor used where a simple `eq(...)` matcher would do
- Mixing classic `when/verify` and `given/then` BDD style in one test class
