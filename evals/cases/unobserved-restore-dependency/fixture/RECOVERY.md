# Recovery contract

The recovery service supplies `REMOTE_SCHEMA_VERSION` at execution time. The
value is intentionally not committed. Operators must use a compatible archive,
but the service endpoint and its current schema identity are external to this
repository.
