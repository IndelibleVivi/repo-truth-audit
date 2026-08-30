# Operator contract

Before any remote write, the operator helper must read `/etc/faye-host-role`
and complete `ROLE_CHECK`. Only after that check succeeds may `REMOTE_WRITE`
begin. This ordering is the release safety invariant.
