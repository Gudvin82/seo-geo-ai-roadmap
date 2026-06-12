# CMS Connectors

`v3.1.0` makes CMS connectors more operational and more explicit about safe
writeback boundaries.

## Supported connectors

- WordPress
- Tilda
- Bitrix
- Webflow

## Current useful scope

- create a connector per project
- sync inventory
- map titles, slugs, status, URL, and metadata fields
- generate governed patch packages
- export suggested changes for human or AI implementation

## Writeback modes

- `read_only`
- `draft`
- `human_approved_publish`

## Safe boundaries

Safe:

- content inventory
- metadata/title/status mapping
- patch suggestions
- schema and llms.txt suggestions
- exportable implementation payloads

Needs human review:

- title rewrites
- schema changes
- publish operations
- client-facing messaging changes

Not supported:

- silent destructive updates
- automatic publish without review

## WordPress notes

The WordPress starter connector is the most useful path in this release. It is
intended to support page fetching, metadata mapping, and exportable suggested
changes before any publishing step is considered.

## RU-market notes

Tilda and Bitrix remain strategically important for RU-market operator flows.
`v3.1.0` documents them as starter connectors with inventory and governed patch
package support.
