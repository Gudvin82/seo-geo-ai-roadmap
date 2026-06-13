# Chrome Extension

This package is a repo-ready Chrome extension for running a passive SEO/GEO/AI
audit against the currently open tab.

## What it does

- stores your self-hosted API base in local extension storage
- sends the active tab URL to `POST /api/v1/scanner/url-audit`
- shows the scan job id plus status and result endpoints

## Local install

1. Open `chrome://extensions`
2. Enable Developer mode
3. Choose **Load unpacked**
4. Select `extensions/chrome/`

## Before store submission

1. review the API base default
2. add icons and screenshots
3. attach privacy disclosure and support URL
4. verify against your production scanner domain
