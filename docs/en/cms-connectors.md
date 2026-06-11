# CMS Connectors

## Current scope

`v2.2.0` introduces a WordPress-first connector direction and documents the
expected patch workflow.

## WordPress

- fetch page and post lists through the REST API
- map URLs, titles, and statuses into audit workflows
- export draft-ready implementation notes
- keep human review mandatory before publication
- starter script: `scripts/wordpress_connector_starter.py`
- starter script: `scripts/wordpress_connector_starter.py`

## Webflow

- documented as a starter path
- recommended for read-only inventory and export-first workflows first
- direct writeback remains roadmap work

## Patch mode expectations

- read-only inventory is safe by default
- generated changes should become tasks, drafts, or diff-like suggestions
- direct publishing should be opt-in and human-reviewed
