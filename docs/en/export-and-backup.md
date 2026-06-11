# Export and Backup

## What to back up

- database
- artifact storage
- `.env` and provider references
- brand facts and project metadata

## What can be exported today

- reports
- artifacts
- provider config templates
- demo dataset through seed flow

## Restore path

1. restore the database
1. restore artifact storage
1. reapply `.env`
1. run migrations if the target version changed
