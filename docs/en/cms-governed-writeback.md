# CMS Governed Writeback

## Modes

- `read_only`: inventory, patch planning, and exports only
- `draft`: draft-safe patch package generation
- `human_approved_publish`: publish package preparation plus explicit human gate

## Safe, risky, and unsupported actions

Safe actions:

- inventory sync
- schema suggestion export
- patch package preparation

Risky actions:

- content overwrite
- bulk patch application
- live publish without page-by-page review

Unsupported actions:

- silent destructive updates
- hidden publish behavior
- unbounded site-wide writeback
