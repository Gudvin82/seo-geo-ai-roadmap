# Extensions and Automation v4.1.0

`v4.1.0` переводит эти поверхности из базовых scaffolds в repo-ready operator
packages:

- GitHub Action: `.github/actions/ai-visibility-check/action.yml`
- VS Code extension package: `extensions/vscode/`
- Chrome extension package: `extensions/chrome/`
- Telegram webhook runtime: `POST /api/v1/telegram/webhook`

Что теперь входит:

- локально устанавливаемые extension packages с README и privacy notes
- реальный Telegram bot command path для `/geo audit`
- честные packaging boundaries для последующей marketplace publication
