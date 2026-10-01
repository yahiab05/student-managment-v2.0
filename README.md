## Testing

Run the wizard tests and the application tests as separate stages:

```bash
QT_QPA_PLATFORM=offscreen pytest -q mysql_wizard/tests
QT_QPA_PLATFORM=offscreen pytest -q app/tests
```

The GitLab pipeline builds `Dockerfile.test`, loads `mysql_wizard/sql/old_schema.sql`
into a disposable `legacy_db`, adds the CI fixtures from `test_seed.sql`, runs the
wizard tests including the database migration, and then runs the application tests.
