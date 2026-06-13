# VS Code Extension

This package turns the repo into an editor-side operator surface.

## Commands

- `SEO GEO AI: Run Audit`
- `SEO GEO AI: Open Summary`
- `SEO GEO AI: Start Agent Mode`

## Settings

- `seoGeoAi.apiBase`
- `seoGeoAi.authToken`

## Local packaging

1. Open the folder in VS Code
2. Install `vsce` if you want a local package build
3. Run `vsce package`
4. Install the resulting `.vsix`

## Before marketplace publication

1. add icon and screenshots
2. confirm publisher ownership
3. verify auth-token handling against production
4. attach privacy and support metadata
