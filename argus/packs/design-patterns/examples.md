## Design Patterns Examples

### Strategy — eliminate type dispatch

```python
# Incorrect — type switch
def format_output(content: str, fmt: str) -> str:
    if fmt == "markdown":
        return f"# {content}"
    elif fmt == "plain":
        return content
    elif fmt == "html":
        return f"<h1>{content}</h1>"

# Correct — Strategy
class OutputStrategy(Protocol):
    def format(self, content: str) -> str: ...

class MarkdownStrategy:
    def format(self, content: str) -> str:
        return f"# {content}"

class HtmlStrategy:
    def format(self, content: str) -> str:
        return f"<h1>{content}</h1>"

class Formatter:
    """Format output using an injected strategy."""

    def __init__(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def format(self, content: str) -> str:
        """Apply the configured strategy to content."""
        return self._strategy.format(content)
```

### Factory — centralise creation

```python
# Incorrect — creation scattered in application code
if platform == "claude":
    adapter = ClaudeAdapter(config)
elif platform == "cursor":
    adapter = CursorAdapter(config)

# Correct — Factory
class AdapterFactory:
    """Create platform adapters by name."""

    _registry: dict[str, type[Adapter]] = {
        "claude": ClaudeAdapter,
        "cursor": CursorAdapter,
    }

    def create(self, platform: str, config: Config) -> Adapter:
        """Return an adapter for the given platform name."""
        cls = self._registry[platform]
        return cls(config)
```

### Observer — decouple state changes from reactions

```python
class GenerationCompleted:
    files: list[GeneratedFile]

class EventBus:
    """Dispatch events to registered subscribers."""

    def __init__(self) -> None:
        self._subscribers: list[Callable[[GenerationCompleted], None]] = []

    def subscribe(self, handler: Callable[[GenerationCompleted], None]) -> None:
        """Register a handler for GenerationCompleted events."""
        self._subscribers.append(handler)

    def publish(self, event: GenerationCompleted) -> None:
        """Notify all subscribers of an event."""
        for handler in self._subscribers:
            handler(event)
```
