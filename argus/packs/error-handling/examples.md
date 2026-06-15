## Error Handling Examples

### Correct
```python
class ArgusError(Exception): ...
class PackNotFoundError(ArgusError): ...  # inherits from base

try:
    adapter.generate(packs)
except (PackNotFoundError, UnknownPlatformError) as e:
    click.echo(f"✗ {e}", err=True)
    sys.exit(1)

raise PackNotFoundError(f'Unknown pack: "{name}"') from None
```

### Incorrect
```python
class PackNotFoundError(Exception): ...   # missing base class
except Exception as e: pass              # swallowed, too broad
except:                                  # bare except
try: ... except SomeError: pass          # silent swallow
```

### Re-raise with context
```python
except yaml.YAMLError as e:
    raise ArgusConfigError("Invalid .argus.yml") from e
```
