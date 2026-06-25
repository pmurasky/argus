## Security Checklist

- [ ] All database queries use parameterized statements — no string interpolation
- [ ] No user input passed to shell commands; subprocess called with argument list, not shell=True
- [ ] No hardcoded secrets, credentials, or API keys in source code
- [ ] All input validated at system boundaries (type, length, format) before processing
- [ ] Allowlist validation used — input rejected if it doesn't match expected pattern
- [ ] Passwords hashed with bcrypt or argon2 before storage
- [ ] Encryption keys stored separately from the data they protect
- [ ] Authorization checked server-side on every request — no client-supplied role trust
- [ ] Session tokens expire and are invalidated on logout
- [ ] External data (deserialised objects, uploads) validated against a schema before use
