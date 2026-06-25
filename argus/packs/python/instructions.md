# Python

## PEP 8 Style
- Indent with 4 spaces — never tabs
- Keep lines within 88 characters (Black default)
- Separate top-level definitions with two blank lines; methods with one
- Group imports as stdlib, third-party, then local, each group blank-line separated

## Naming Conventions
- Use snake_case for variables, functions, and modules; PascalCase for classes
- Use UPPER_SNAKE_CASE for module-level constants
- Prefix internal names with a single underscore; reserve double underscore for name-mangling
- Avoid single-letter names except loop indices; never shadow builtins like list, id, or type

## Idiomatic Python
- Prefer f-strings over .format() or % interpolation
- Use comprehensions over explicit loops for simple transforms
- Manage every resource (files, locks, connections) with a with statement
- Use pathlib.Path for filesystem paths instead of os.path string manipulation
- Iterate with enumerate() and zip() instead of manual index arithmetic
- Compare to None with is and is not, never == or !=

## Dataclasses and Data Structures
- Use @dataclass for structured data containers instead of bare dicts
- Use @dataclass(frozen=True) for immutable value objects
- Prefer a @dataclass or namedtuple over a positional tuple when fields carry meaning
- Reserve dict for genuinely dynamic key-value maps; use a dataclass for fixed schemas

## Red Flags — Stop and Correct
- String built with .format() or % where an f-string is clearer
- Manual file .close() instead of a with statement
- os.path.join chains where pathlib.Path / would read better
- Bare dict passed around as an implicit record with fixed fields
- Variable or function named in camelCase or a class named in snake_case
- == None or != None instead of is None / is not None
