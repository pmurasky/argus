# Security

## Input Validation
- Use allowlists, not blocklists — define what is permitted, reject everything else
- Validate type, length, and format before any processing
- Reject input that does not conform — never sanitize-and-proceed
- Validate at every system boundary, including internal service calls

## A03 Injection
- Use parameterized queries or prepared statements for all database access
- Never pass user input to shell commands; use subprocess with argument lists, not shell=True
- Treat all external input as untrusted regardless of source (user, API, file, environment)

## A02 Cryptographic Failures
- Never store secrets or credentials in source code or version control
- Use a well-established library (e.g. cryptography, bcrypt) — never hand-roll crypto primitives
- Prefer asymmetric or hash-based solutions over symmetric encryption for secrets at rest
- Store encryption keys separately from the data they protect

## A01 Broken Access Control
- Enforce authorization on every request at the server side — never trust client-supplied roles or IDs
- Use deny-by-default: grant minimum permissions required, not broad access trimmed down
- Validate that the authenticated user owns the resource being accessed before returning it

## A07 Identification and Authentication Failures
- Never hardcode credentials, tokens, or API keys — use environment variables or a secrets manager
- Hash passwords with a slow algorithm (bcrypt, argon2) before storage — never store plaintext or MD5/SHA-1
- Expire and rotate session tokens; invalidate them on logout

## A04 Insecure Design
- Model threat scenarios at design time — identify trust boundaries and adversarial inputs before writing code
- Never implement security controls as optional flags or commented-out blocks
- Separate concerns: authentication, authorization, and business logic belong in distinct layers

## A08 Software and Data Integrity Failures
- Verify the integrity of external data (deserialised objects, uploaded files) before processing
- Never deserialize data from untrusted sources without schema validation
- Treat deserialization of user-supplied pickle, YAML with arbitrary tags, or XML as high-risk

## Red Flags — Stop and Correct
- User input used in SQL query without parameterization
- User input passed to a shell command (especially shell=True)
- Hardcoded secret, credential, or API key in source code
- Missing input validation before database write or external API call
- Symmetric encryption key stored in the same codebase as the ciphertext
- Authentication check bypassed with a flag or commented out
