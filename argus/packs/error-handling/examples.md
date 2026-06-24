## Error Handling Examples

### Correct
```python
class AppError(Exception): ...
class ResourceNotFoundError(AppError): ...  # inherits from base

try:
    service.process(items)
except (ResourceNotFoundError, ConfigError) as e:
    click.echo(f"✗ {e}", err=True)
    sys.exit(1)

raise ResourceNotFoundError(f'Unknown resource: "{name}"') from None
```

### Incorrect
```python
class ResourceNotFoundError(Exception): ...   # missing base class
except Exception as e: pass                    # swallowed, too broad
except:                                        # bare except
try: ... except SomeError: pass                # silent swallow
```

### Re-raise with context
```python
except yaml.YAMLError as e:
    raise AppConfigError("Invalid config file") from e
```
