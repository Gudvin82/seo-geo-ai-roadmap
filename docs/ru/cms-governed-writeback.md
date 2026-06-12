# Governed CMS Writeback

## Режимы

- `read_only`: только inventory, patch planning и exports
- `draft`: draft-safe подготовка patch package
- `human_approved_publish`: подготовка publish package плюс явный human gate

## Safe, risky и unsupported actions

Safe actions:

- inventory sync
- schema suggestion export
- patch package preparation

Risky actions:

- content overwrite
- bulk patch application
- live publish без page-by-page review

Unsupported actions:

- silent destructive updates
- hidden publish behavior
- unbounded site-wide writeback
